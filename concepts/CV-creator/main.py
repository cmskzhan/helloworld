import os
import json
from typing import List, Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import logging

from core_profiling import (
    load_profile, save_profile, delete_profile, get_profile_text, 
    merge_profiles, extract_text_from_bytes, extract_structured_data,
    DEDUPLICATION_PROMPT, TRAINING_DATA_DIR
)
from core_cv import create_pdf_bytes, create_docx_bytes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Local AI CV Tailor & Profiling API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ModelRequest(BaseModel):
    api_key: str

class ProfileGenerateRequest(BaseModel):
    jd: str
    use_profile: bool
    focus: str
    api_key: str
    model_name: str

class MarkdownExportRequest(BaseModel):
    markdown: str

class DeduplicateRequest(BaseModel):
    api_key: str
    model_name: str
    profile: dict

@app.post("/api/models")
def get_models(req: ModelRequest):
    if not req.api_key:
        raise HTTPException(status_code=400, detail="API Key required")
    try:
        logger.info("Fetching models from Google GenAI API")
        client = genai.Client(api_key=req.api_key)
        models = client.models.list()
        # Sort so pro/flash are first
        dynamic = sorted([m.name for m in models], 
                        key=lambda x: ("flash" in x.lower() or "pro" in x.lower()), 
                        reverse=True)
        if dynamic:
            logger.info(f"Discovered {len(dynamic)} models")
            return {"models": dynamic}
        return {"models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp"]}
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
def scan_training_data(api_key: str = Form(...), model_name: str = Form(...)):
    if not TRAINING_DATA_DIR.exists():
        TRAINING_DATA_DIR.mkdir(parents=True, exist_ok=True)
    md_files = sorted(list(TRAINING_DATA_DIR.glob("*.md")))
    if not md_files:
        return {"scanned": 0, "message": "No markdown files found"}
    
    try:
        client = genai.Client(api_key=api_key)
        profile = load_profile()
        for f in md_files:
            try:
                with open(f, "r", encoding="utf-8") as file:
                    cv_text = file.read()
                if not cv_text.strip(): continue
                extracted = extract_structured_data(cv_text, client, model_name)
                profile = merge_profiles(profile, extracted, source_file=f.name)
            except Exception as e:
                logger.error(f"Error processing {f.name}: {e}")
        save_profile(profile)
        return {"scanned": len(md_files), "profile": profile}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/profile/extract")
async def extract_upload(
    api_key: str = Form(...), 
    model_name: str = Form(...), 
    files: List[UploadFile] = File(...)
):
    try:
        client = genai.Client(api_key=api_key)
        profile = load_profile()
        for f in files:
            content = await f.read()
            if f.filename.lower().endswith(".md"):
                cv_text = content.decode("utf-8")
            else:
                cv_text = extract_text_from_bytes(content, f.filename)
            if not cv_text.strip(): continue
            extracted = extract_structured_data(cv_text, client, model_name)
            profile = merge_profiles(profile, extracted, source_file=f.filename)
        save_profile(profile)
        return {"profile": profile}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/profile/deduplicate")
def deduplicate_profile(req: DeduplicateRequest):
    try:
        client = genai.Client(api_key=req.api_key)
        profile_json = json.dumps(req.profile, indent=2, ensure_ascii=False)
        prompt = DEDUPLICATION_PROMPT.format(profile_json=profile_json)
        response = client.models.generate_content(
            model=req.model_name,
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        raw = response.text.strip()
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
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cv/generate")
async def generate_cv(
    jd: str = Form(...),
    use_profile: bool = Form(...),
    focus: str = Form(...),
    api_key: str = Form(...),
    model_name: str = Form(...),
    files: Optional[List[UploadFile]] = File(None)
):
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
        - Use Markdown (H1 for Name, H2 for Sections).
        - Focus on: {focus}
        - Match keywords from the JD naturally.
        - Ensure bullet points are achievement-oriented.
        """
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model_name, contents=prompt)
        return {"markdown": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cv/pdf")
def export_pdf(req: MarkdownExportRequest):
    try:
        pdf_bytes = create_pdf_bytes(req.markdown)
        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cv/docx")
def export_docx(req: MarkdownExportRequest):
    try:
        docx_bytes = create_docx_bytes(req.markdown)
        return Response(content=docx_bytes, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files as fallback - API takes precedence
app.mount("/", StaticFiles(directory="static", html=True), name="static")
