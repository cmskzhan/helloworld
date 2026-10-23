import os
import json
from typing import List, Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from claude_client import (
    get_available_models,
    resolve_model_id,
    get_client,
    generate_text,
    classify_claude_error,
)
from core_profiling import (
    load_profile, save_profile, delete_profile, get_profile_text,
    merge_profiles, extract_text_from_bytes, extract_structured_data,
    DEDUPLICATION_PROMPT, TRAINING_DATA_DIR
)
from core_cv import create_pdf_bytes, create_docx_bytes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Local AI CV Tailor & Profiling API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MarkdownExportRequest(BaseModel):
    markdown: str

class DeduplicateRequest(BaseModel):
    model_name: str
    profile: dict

@app.get("/api/models")
def get_models():
    models = get_available_models()
    if not models:
        raise HTTPException(
            status_code=500,
            detail=(
                "No Claude models configured on the server. Set at least one of "
                "CLAUDE_SONNET_MODEL_ID, CLAUDE_OPUS_MODEL_ID in .env "
                "(see .env.example)."
            ),
        )
    return {"models": list(models.keys())}

@app.get("/api/profile")
def get_profile():
    return load_profile()

@app.post("/api/profile")
def save_profile_endpoint(profile: dict):
    save_profile(profile)
    return {"status": "success"}

@app.delete("/api/profile")
def reset_profile_endpoint():
    delete_profile()
    return {"status": "success"}

@app.get("/api/profile/text")
def get_profile_text_endpoint():
    return {"text": get_profile_text()}

@app.post("/api/profile/scan")
def scan_training_data(model_name: str = Form(...)):
    model_id = resolve_model_id(model_name)
    if not model_id:
        raise HTTPException(status_code=400, detail="Unknown model")
    if not TRAINING_DATA_DIR.exists():
        TRAINING_DATA_DIR.mkdir(parents=True, exist_ok=True)
    md_files = sorted(list(TRAINING_DATA_DIR.glob("*.md")))
    if not md_files:
        return {"scanned": 0, "message": "No markdown files found"}

    try:
        client = get_client()
        profile = load_profile()
        for f in md_files:
            try:
                with open(f, "r", encoding="utf-8") as file:
                    cv_text = file.read()
                if not cv_text.strip(): continue
                extracted = extract_structured_data(cv_text, client, model_id)
                profile = merge_profiles(profile, extracted, source_file=f.name)
            except Exception as e:
                logger.exception(f"Error processing {f.name} (model={model_id})")
        save_profile(profile)
        return {"scanned": len(md_files), "profile": profile}
    except Exception as e:
        logger.exception(f"/api/profile/scan failed (model={model_id})")
        status_code, message = classify_claude_error(e)
        raise HTTPException(status_code=status_code, detail=message)

@app.post("/api/profile/extract")
async def extract_upload(
    model_name: str = Form(...),
    files: List[UploadFile] = File(...)
):
    model_id = resolve_model_id(model_name)
    if not model_id:
        raise HTTPException(status_code=400, detail="Unknown model")
    try:
        client = get_client()
        profile = load_profile()
        for f in files:
            content = await f.read()
            if f.filename.lower().endswith(".md"):
                cv_text = content.decode("utf-8")
            else:
                cv_text = extract_text_from_bytes(content, f.filename)
            if not cv_text.strip(): continue
            extracted = extract_structured_data(cv_text, client, model_id)
            profile = merge_profiles(profile, extracted, source_file=f.filename)
        save_profile(profile)
        return {"profile": profile}
    except Exception as e:
        logger.exception(f"/api/profile/extract failed (model={model_id})")
        status_code, message = classify_claude_error(e)
        raise HTTPException(status_code=status_code, detail=message)

@app.post("/api/profile/deduplicate")
def deduplicate_profile(req: DeduplicateRequest):
    model_id = resolve_model_id(req.model_name)
    if not model_id:
        raise HTTPException(status_code=400, detail="Unknown model")
    try:
        client = get_client()
        profile_json = json.dumps(req.profile, indent=2, ensure_ascii=False)
        prompt = DEDUPLICATION_PROMPT.format(profile_json=profile_json)
        raw = generate_text(client, model_id, prompt).strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            if raw.endswith("```"): raw = raw[: raw.rfind("```")]
        deduped = json.loads(raw)
        
        # Keep original metadata but update last updated
        import datetime
        deduped["metadata"] = req.profile.get("metadata", {})
        deduped["metadata"]["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return {"profile": deduped}
    except Exception as e:
        logger.exception(f"/api/profile/deduplicate failed (model={model_id})")
        status_code, message = classify_claude_error(e)
        raise HTTPException(status_code=status_code, detail=message)

@app.post("/api/cv/generate")
async def generate_cv(
    jd: str = Form(...),
    use_profile: bool = Form(...),
    focus: str = Form(...),
    model_name: str = Form(...),
    files: Optional[List[UploadFile]] = File(None)
):
    model_id = resolve_model_id(model_name)
    if not model_id:
        raise HTTPException(status_code=400, detail="Unknown model")
    try:
        context_text = ""
        if use_profile:
            context_text += get_profile_text() + "\n\n"
        
        if files:
            for f in files:
                content = await f.read()
                if f.filename.lower().endswith(".md"):
                    context_text += content.decode("utf-8")
                else:
                    context_text += extract_text_from_bytes(content, f.filename)
        
        prompt = f"""
        You are an expert CV writer. Create a professional CV in Markdown.
        
        JOB DESCRIPTION:
        {jd}
        
        CANDIDATE DATA:
        {context_text}
        
        REQUIREMENTS:
        - Use Markdown with the following exact structure:
          1. H1 for Name (e.g., # FULL NAME)
          2. Contact line: **Email** | email@example.com | **Phone** | +1234567 | **Location** | City, Country | **LinkedIn** | linkedin.com/in/user
          3. ## Professional Summary (2-3 sentences, tailored to the JD)
          4. ## Technical Skills
          5. ## Work Experience
          6. ## Education
          7. ## Certifications (if applicable)
          8. ## Projects (if applicable)
        - For each job, use this exact format:
          **Job Title** | Company Name | Location | Start Date - End Date
          - Achievement bullet 1
          - Achievement bullet 2
        - For skills, use: **Category:** item1, item2, item3
        - Focus on: {focus}
        - Match keywords from the JD naturally.
        - Ensure bullet points are achievement-oriented with measurable outcomes.
        - Do NOT use markdown tables, horizontal rules (---), or inline code blocks.
        - Do NOT use ### headers — use **Title** | Company pattern for job entries.
        - Omit empty sections entirely.
        """
        client = get_client()
        markdown = generate_text(client, model_id, prompt)
        return {"markdown": markdown}
    except Exception as e:
        logger.exception(f"/api/cv/generate failed (model={model_name} -> {model_id})")
        status_code, message = classify_claude_error(e)
        raise HTTPException(status_code=status_code, detail=message)

@app.post("/api/cv/pdf")
def export_pdf(req: MarkdownExportRequest):
    try:
        pdf_bytes = create_pdf_bytes(req.markdown)
        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        logger.exception("/api/cv/pdf failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cv/docx")
def export_docx(req: MarkdownExportRequest):
    try:
        docx_bytes = create_docx_bytes(req.markdown)
        return Response(content=docx_bytes, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception as e:
        logger.exception("/api/cv/docx failed")
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files as fallback - API takes precedence
app.mount("/", StaticFiles(directory="static", html=True), name="static")
