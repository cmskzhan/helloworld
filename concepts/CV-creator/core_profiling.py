import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from docx import Document
from pypdf import PdfReader
import re

PROFILE_PATH = Path(__file__).parent / "user_profile.json"
TRAINING_DATA_DIR = Path(__file__).parent / "trainingData"

PROFILE_SCHEMA = {
    "personal_info": {"full_name": "", "email": "", "phone": "", "location": "", "linkedin": "", "github": "", "website": "", "summary": ""},
    "work_experience": [],
    "education": [],
    "skills": {"technical": [], "soft": [], "languages": [], "certifications": []},
    "projects": [],
    "publications": [],
    "awards": [],
    "metadata": {"last_updated": "", "source_files": []},
}

EXTRACTION_PROMPT = """
You are a CV/resume data extraction expert. Analyse the following CV text and
return a **valid JSON object** (no markdown fences, no commentary) that matches
this exact schema. Fill in every field you can find; leave fields as empty
strings or empty lists if the information is not present.

SCHEMA:
{schema}

CV TEXT:
{cv_text}

RULES:
1. Return ONLY the JSON object — no extra text.
2. Dates should be in "MMM YYYY" format (e.g. "Jan 2020") or "Present".
3. Preserve the original wording of achievements and responsibilities.
4. If a section appears more than once (e.g. multiple jobs), return all entries.
5. For skills, separate into technical, soft, languages, and certifications.
"""

DEDUPLICATION_PROMPT = """
You are a data deduplication expert. The following JSON represents a person's
CV profile that was aggregated from many different CV versions. It contains
many duplicate and near-duplicate entries across all sections.

Your task is to **deduplicate and consolidate** this profile into a single,
clean version. Return a **valid JSON object** with the exact same schema.

PROFILE JSON:
{profile_json}

RULES:
1. Return ONLY the valid JSON object — no markdown fences, no commentary.
2. **work_experience**: Merge entries that refer to the same role at the same
   company into ONE entry. Combine all unique responsibilities and achievements
   from duplicates into the merged entry. Normalise the key to "job_title"
   (not "position", "role", or "title"). Keep the most complete date range.
   Order chronologically (most recent first).
3. **education**: Merge entries for the same degree at the same institution.
   Normalise keys to "degree", "institution", "start_date", "end_date",
   "details". Remove fields like "field_of_study" by folding them into
   "degree" (e.g. "MPhil Computer Science").
4. **skills**: Remove exact and near-duplicate skills (e.g. "kubernetes" and
   "k8s" keep one, "Shell Scripting" and "Shell script" keep one,
   "Unix/Linux" and "Linux" keep the more descriptive one). Sort each list
   alphabetically.
5. **projects**: Merge entries that refer to the same project. Normalise keys
   to "name", "description", "technologies", "url".
6. **awards**: Normalise all entries to objects with keys "title", "date",
   "issuer". Remove duplicates. If both a string and an object refer to the
   same award, keep only the object form.
7. **publications**: Deduplicate.
8. **personal_info**: Keep the most complete value for each field.
9. **metadata**: Keep as-is.
10. Do NOT discard any genuinely unique information — only merge duplicates.
"""

def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    from io import BytesIO
    name = filename.lower()
    if name.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".doc"):
        with tempfile.NamedTemporaryFile(suffix=".doc", delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        try:
            result = subprocess.run(["antiword", tmp_path], capture_output=True, text=True, check=True)
            return result.stdout
        finally:
            os.unlink(tmp_path)
    doc = Document(BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)

def load_profile() -> dict:
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.loads(json.dumps(PROFILE_SCHEMA))

def save_profile(profile: dict) -> None:
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

def delete_profile() -> bool:
    if PROFILE_PATH.exists():
        PROFILE_PATH.unlink()
        return True
    return False

def get_profile_text(profile: dict = None) -> str:
    """Return profile as markdown matching the CV template structure."""
    if profile is None:
        profile = load_profile()
    lines = []
    pi = profile.get("personal_info", {})
    
    # Name as H1
    if pi.get("full_name"):
        lines.append(f"# {pi['full_name']}")
        lines.append("")
    
    # Contact line in template format: **Label** | value | **Label** | value
    contact_parts = []
    if pi.get("email"): contact_parts.append(f"**Email** | {pi['email']}")
    if pi.get("phone"): contact_parts.append(f"**Phone** | {pi['phone']}")
    if pi.get("location"): contact_parts.append(f"**Location** | {pi['location']}")
    if pi.get("linkedin"): contact_parts.append(f"**LinkedIn** | {pi['linkedin']}")
    if pi.get("github"): contact_parts.append(f"**GitHub** | {pi['github']}")
    if pi.get("website"): contact_parts.append(f"**Website** | {pi['website']}")
    if contact_parts:
        lines.append(" | ".join(contact_parts))
        lines.append("")
    
    # Summary
    if pi.get("summary"):
        lines.append("## Professional Summary")
        lines.append("")
        lines.append(pi['summary'])
        lines.append("")
    
    # Work Experience
    work = profile.get("work_experience", [])
    if work:
        lines.append("## Work Experience")
        lines.append("")
        for job in work:
            title = job.get("job_title", "")
            company = job.get("company", "")
            loc = job.get("location", "")
            dates = f"{job.get('start_date', '')} - {job.get('end_date', '')}"
            lines.append(f"**{title}** | {company} | {loc} | {dates}")
            lines.append("")
            for r in job.get("responsibilities", []):
                lines.append(f"- {r}")
            for a in job.get("achievements", []):
                lines.append(f"- {a}")
            lines.append("")
    
    # Education
    edu = profile.get("education", [])
    if edu:
        lines.append("## Education")
        lines.append("")
        for e in edu:
            degree = e.get("degree", "")
            inst = e.get("institution", "")
            loc = e.get("location", "")
            dates = f"{e.get('start_date', '')} - {e.get('end_date', '')}"
            lines.append(f"**{degree}** | {inst} | {loc} | {dates}")
            lines.append("")
            if e.get("details"):
                lines.append(f"- {e['details']}")
                lines.append("")
    
    # Skills
    skills = profile.get("skills", {})
    if any(skills.get(k) for k in ("technical", "soft", "languages", "certifications")):
        lines.append("## Technical Skills")
        lines.append("")
        if skills.get("technical"):
            lines.append(f"**Technical:** {', '.join(skills['technical'])}")
        if skills.get("soft"):
            lines.append(f"**Soft Skills:** {', '.join(skills['soft'])}")
        if skills.get("languages"):
            lines.append(f"**Languages:** {', '.join(skills['languages'])}")
        lines.append("")
    
    # Certifications (separate section if present)
    if skills.get("certifications"):
        lines.append("## Certifications")
        lines.append("")
        for cert in skills["certifications"]:
            lines.append(f"- {cert}")
        lines.append("")
    
    # Projects
    projects = profile.get("projects", [])
    if projects:
        lines.append("## Projects")
        lines.append("")
        for p in projects:
            lines.append(f"**{p.get('name', '')}** | {p.get('description', '')}")
            lines.append("")
            if p.get("technologies"):
                lines.append(f"- Technologies: {', '.join(p['technologies'])}")
            if p.get("url"):
                lines.append(f"- URL: {p['url']}")
            lines.append("")
    
    # Publications
    pubs = profile.get("publications", [])
    if pubs:
        lines.append("## Publications")
        lines.append("")
        for pub in pubs:
            lines.append(f"- {pub}")
        lines.append("")
    
    # Awards
    awards = profile.get("awards", [])
    if awards:
        lines.append("## Awards")
        lines.append("")
        for a in awards:
            lines.append(f"- {a}")
        lines.append("")
    
    return "\n".join(lines)

def _merge_list_of_dicts(existing: list, incoming: list, key_fields: list) -> list:
    seen = set()
    for item in existing:
        values = []
        for k in key_fields: val = str(item.get(k, "")); values.append(val.strip().lower())
        seen.add(tuple(values))
    merged = list(existing)
    for item in incoming:
        values = []
        for k in key_fields: val = str(item.get(k, "")); values.append(val.strip().lower())
        sig = tuple(values)
        if sig not in seen:
            merged.append(item)
            seen.add(sig)
    return merged

def _merge_unique_strings(existing: list, incoming: list) -> list:
    def _to_clean_str(s): return str(s).strip().lower()
    seen = {_to_clean_str(s) for s in existing}
    merged = list(existing)
    for s in incoming:
        clean_s = _to_clean_str(s)
        if clean_s not in seen:
            merged.append(s)
            seen.add(clean_s)
    return merged

def merge_profiles(existing: dict, new_data: dict, source_file: str = "") -> dict:
    for field, value in new_data.get("personal_info", {}).items():
        if value and not existing.get("personal_info", {}).get(field):
            existing.setdefault("personal_info", {})[field] = value
    existing["work_experience"] = _merge_list_of_dicts(existing.get("work_experience", []), new_data.get("work_experience", []), ["job_title", "company"])
    existing["education"] = _merge_list_of_dicts(existing.get("education", []), new_data.get("education", []), ["degree", "institution"])
    for category in ("technical", "soft", "languages", "certifications"):
        existing.setdefault("skills", {})[category] = _merge_unique_strings(existing.get("skills", {}).get(category, []), new_data.get("skills", {}).get(category, []))
    existing["projects"] = _merge_list_of_dicts(existing.get("projects", []), new_data.get("projects", []), ["name"])
    existing["publications"] = _merge_unique_strings(existing.get("publications", []), new_data.get("publications", []))
    existing["awards"] = _merge_unique_strings(existing.get("awards", []), new_data.get("awards", []))
    existing.setdefault("metadata", {})["last_updated"] = datetime.now(timezone.utc).isoformat()
    sources = existing.get("metadata", {}).get("source_files", [])
    if source_file and source_file not in sources:
        sources.append(source_file)
    existing["metadata"]["source_files"] = sources
    return existing

def extract_structured_data(cv_text: str, client, model_name: str) -> dict:
    schema_json = json.dumps(PROFILE_SCHEMA, indent=2)
    prompt = EXTRACTION_PROMPT.format(schema=schema_json, cv_text=cv_text)
    response = client.models.generate_content(model=model_name, contents=prompt, config={'response_mime_type': 'application/json'})
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"): raw = raw[: raw.rfind("```")]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match: return json.loads(match.group(0))
        raise
