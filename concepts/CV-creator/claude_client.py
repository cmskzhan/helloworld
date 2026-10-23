import logging
import os
import subprocess
import threading
from pathlib import Path
from dotenv import load_dotenv
import boto3
from anthropic import (
    AnthropicBedrock,
    AuthenticationError,
    PermissionDeniedError,
    RateLimitError,
    APIConnectionError,
    APIStatusError,
)
from botocore.exceptions import ProfileNotFound, NoCredentialsError, BotoCoreError

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

logger = logging.getLogger(__name__)

# Env var holding each model id/ARN, with the label to fall back on when the
# underlying foundation model can't be looked up from Bedrock.
MODEL_ENV_VARS = {
    "CLAUDE_SONNET_MODEL_ID": "Claude Sonnet",
    "CLAUDE_OPUS_MODEL_ID": "Claude Opus",
}

_label_cache: dict[str, str] = {}


def _prettify_model_name(model_arn: str) -> str:
    """anthropic.claude-haiku-4-5-20251001-v1:0 -> 'Claude Haiku 4.5'"""
    base = model_arn.rsplit("/", 1)[-1].split(":", 1)[0]
    words, nums = [], []
    for token in base.split(".")[-1].split("-"):
        if token.isdigit():
            # 8-digit tokens are release datestamps, not version numbers.
            if len(token) != 8:
                nums.append(token)
        elif not (token.startswith("v") and token[1:].isdigit()):
            words.append(token.capitalize())
    return " ".join(words) + (f" {'.'.join(nums)}" if nums else "")


def _resolve_label(model_id: str, fallback: str) -> str:
    """Name the dropdown entry after the foundation model the id actually points at."""
    if model_id in _label_cache:
        return _label_cache[model_id]

    model_arn = model_id
    if "application-inference-profile/" in model_id:
        try:
            bedrock = boto3.Session(
                profile_name=os.environ.get("AWS_PROFILE"),
                region_name=os.environ.get("AWS_REGION"),
            ).client("bedrock")
            profile = bedrock.get_inference_profile(inferenceProfileIdentifier=model_id)
            model_arn = profile["models"][0]["modelArn"]
        except Exception as e:
            # Not cached, so a later request retries once credentials are usable again.
            logger.warning(f"Could not resolve inference profile for {fallback}: {e}")
            return fallback

    label = _prettify_model_name(model_arn) or fallback
    _label_cache[model_id] = label
    return label


def get_available_models() -> dict[str, str]:
    """UI-facing label -> Bedrock model id/ARN, for every model configured via env."""
    models = {}
    for env_var, fallback in MODEL_ENV_VARS.items():
        model_id = os.environ.get(env_var)
        if model_id:
            models[_resolve_label(model_id, fallback)] = model_id
    return models


def resolve_model_id(label: str) -> str | None:
    """Look up a label from the dropdown. Also accepts the unresolved fallback labels,
    so a page loaded before Bedrock became reachable can still generate."""
    models = get_available_models()
    if label in models:
        return models[label]
    for env_var, fallback in MODEL_ENV_VARS.items():
        if label == fallback:
            return os.environ.get(env_var)
    return None


def get_client() -> AnthropicBedrock:
    guardrail_id = os.environ.get("BEDROCK_GUARDRAIL_ID")
    guardrail_version = os.environ.get("BEDROCK_GUARDRAIL_VERSION")
    default_headers = None
    if guardrail_id:
        default_headers = {
            "X-Amzn-Bedrock-GuardrailIdentifier": guardrail_id,
            "X-Amzn-Bedrock-GuardrailVersion": guardrail_version or "DRAFT",
        }
    return AnthropicBedrock(
        aws_profile=os.environ.get("AWS_PROFILE"),
        aws_region=os.environ.get("AWS_REGION"),
        default_headers=default_headers,
    )


def generate_text(client: AnthropicBedrock, model_id: str, prompt: str, max_tokens: int = 4096) -> str:
    response = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    raise ValueError("No text block in Claude response")


_refresh_lock = threading.Lock()
_refresh_in_flight = False


def _is_expired_token_error(e: Exception) -> bool:
    text = str(e).lower()
    return "security token" in text or "expired" in text


def _clear_bedrock_session_cache() -> None:
    """Drop anthropic's cached boto3 session so the next call re-resolves credentials
    from disk instead of reusing the frozen (possibly stale) Credentials object."""
    from anthropic.lib.bedrock._auth import _get_session

    _get_session.cache_clear()


def _refresh_credentials_background() -> None:
    """Fire-and-forget: run dexter to renew the AWS session, then drop the cached
    Bedrock session so the *next* request re-resolves fresh credentials from disk.
    This request still fails; it's the one after it that benefits."""
    global _refresh_in_flight
    with _refresh_lock:
        if _refresh_in_flight:
            logger.info("Credential refresh already in flight, not starting another")
            return
        _refresh_in_flight = True

    def _run():
        global _refresh_in_flight
        profile = os.environ.get("AWS_PROFILE", "")
        cmd = ["dexter", "creds", "aws", "--profile", profile, "--script"]
        try:
            logger.warning(f"Bedrock rejected an expired AWS token; refreshing via: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                logger.info(f"dexter creds aws succeeded for profile '{profile}'")
            else:
                logger.error(
                    f"dexter creds aws exited {result.returncode} for profile '{profile}'. "
                    f"stdout: {result.stdout[-2000:]!r} stderr: {result.stderr[-2000:]!r}"
                )
        except subprocess.TimeoutExpired:
            logger.error(
                f"dexter creds aws timed out after 120s for profile '{profile}' -- it likely "
                "hit an interactive LDAP/browser prompt. Run it manually in a terminal."
            )
        except FileNotFoundError:
            logger.error("dexter CLI not found on PATH; cannot auto-refresh AWS credentials.")
        except Exception:
            logger.exception("Unexpected error while refreshing AWS credentials via dexter")
        finally:
            _clear_bedrock_session_cache()
            with _refresh_lock:
                _refresh_in_flight = False

    threading.Thread(target=_run, daemon=True, name="dexter-creds-refresh").start()


def classify_claude_error(e: Exception) -> tuple[int, str]:
    """Map a Bedrock/Claude call failure to (http_status_code, user_facing_message)."""
    if isinstance(e, (AuthenticationError, PermissionDeniedError)):
        if _is_expired_token_error(e):
            _refresh_credentials_background()
            return 502, (
                "AWS session token expired. A credential refresh via dexter has been "
                "triggered in the background -- retry in a few seconds."
            )
        return 502, (
            "AWS credentials were rejected by Bedrock (not an expired token -- check IAM "
            "permissions/guardrail config). Refresh your AWS credentials and try again."
        )
    if isinstance(e, (ProfileNotFound, NoCredentialsError)):
        return 500, (
            "No usable AWS credentials found for the configured AWS_PROFILE. Check "
            "AWS_PROFILE/AWS_REGION in .env and that ~/.aws is set up correctly."
        )
    if isinstance(e, RateLimitError):
        return 429, "Bedrock rate limit hit. Wait a moment and try again."
    if isinstance(e, APIConnectionError):
        return 502, "Could not reach AWS Bedrock. Check network connectivity and AWS_REGION."
    if isinstance(e, APIStatusError):
        return 502, f"Bedrock returned an error (HTTP {e.status_code}): {e.body}"
    if isinstance(e, BotoCoreError):
        return 500, f"AWS SDK error: {e}"
    return 500, str(e)
