"""
User CV Profiling System

Extracts structured data from uploaded CVs and caches it in user_profile.json.
This eliminates the need to re-upload old CVs when creating a new tailored CV.

Usage (standalone):
    streamlit run userCVprofiling.py

Usage (as a module):
    from userCVprofiling import load_profile, get_profile_text
"""

import streamlit as st
from google import genai
from docx import Document
from pypdf import PdfReader
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────────────
PROFILE_PATH = Path(__file__).parent / "user_profile.json"
TRAINING_DATA_DIR = Path(__file__).parent / "trainingData"

PROFILE_SCHEMA = {
    "personal_info": {
        "full_name": "",
        "email": "",
        "phone": "",
        "location": "",
        "linkedin": "",
        "github": "",
        "website": "",
        "summary": "",
    },
    "work_experience": [],
    # Each entry: {
    #     "job_title": str,
    #     "company": str,
    #     "location": str,
    #     "start_date": str,
    #     "end_date": str,
    #     "responsibilities": [str],
    #     "achievements": [str],
    # }
    "education": [],
    # Each entry: {
    #     "degree": str,
    #     "institution": str,
    #     "location": str,
    #     "start_date": str,
    #     "end_date": str,
    #     "details": str,
    # }
    "skills": {
        "technical": [],
        "soft": [],
        "languages": [],
        "certifications": [],
    },
    "projects": [],
    # Each entry: {
    #     "name": str,
    #     "description": str,
    #     "technologies": [str],
    #     "url": str,
    # }
    "publications": [],
    "awards": [],
    "metadata": {
        "last_updated": "",
        "source_files": [],
    },
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


# ── File Text Extraction ────────────────────────────────────────────────────
def extract_text_from_file(uploaded_file) -> str:
    """Extract plain text from an uploaded Streamlit file (PDF, DOCX, DOC)."""
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if name.endswith(".doc"):
        # Legacy .doc — use macOS textutil
        with tempfile.NamedTemporaryFile(suffix=".doc", delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        try:
            txt_path = tmp_path.replace(".doc", ".txt")
            subprocess.run(
                ["textutil", "-convert", "txt", tmp_path, "-output", txt_path],
                check=True,
            )
            with open(txt_path, "r") as f:
                text = f.read()
            os.unlink(txt_path)
            return text
        finally:
            os.unlink(tmp_path)

    # Default: .docx
    doc = Document(uploaded_file)
    return "\n".join(p.text for p in doc.paragraphs)


# ── Profile I/O ─────────────────────────────────────────────────────────────
def load_profile() -> dict:
    """Load existing profile from disk, or return an empty schema."""
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.loads(json.dumps(PROFILE_SCHEMA))  # deep copy


def save_profile(profile: dict) -> None:
    """Write profile dict to user_profile.json."""
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)


def delete_profile() -> bool:
    """Delete user_profile.json. Returns True if file was deleted."""
    if PROFILE_PATH.exists():
        PROFILE_PATH.unlink()
        return True
    return False


def get_profile_text(profile: dict | None = None) -> str:
    """
    Flatten the profile into a human-readable text block suitable for
    injecting into an LLM prompt (used by CV-creator.py).
    """
    if profile is None:
        profile = load_profile()

    lines: list[str] = []
    pi = profile.get("personal_info", {})
    if pi.get("full_name"):
        lines.append(f"Name: {pi['full_name']}")
    if pi.get("email"):
        lines.append(f"Email: {pi['email']}")
    if pi.get("phone"):
        lines.append(f"Phone: {pi['phone']}")
    if pi.get("location"):
        lines.append(f"Location: {pi['location']}")
    if pi.get("linkedin"):
        lines.append(f"LinkedIn: {pi['linkedin']}")
    if pi.get("github"):
        lines.append(f"GitHub: {pi['github']}")
    if pi.get("website"):
        lines.append(f"Website: {pi['website']}")
    if pi.get("summary"):
        lines.append(f"\nProfessional Summary:\n{pi['summary']}")

    # Work experience
    work = profile.get("work_experience", [])
    if work:
        lines.append("\n--- WORK EXPERIENCE ---")
        for job in work:
            title = job.get("job_title", "")
            company = job.get("company", "")
            loc = job.get("location", "")
            dates = f"{job.get('start_date', '')} - {job.get('end_date', '')}"
            lines.append(f"\n{title} at {company} ({loc}) | {dates}")
            for r in job.get("responsibilities", []):
                lines.append(f"  - {r}")
            for a in job.get("achievements", []):
                lines.append(f"  * {a}")

    # Education
    edu = profile.get("education", [])
    if edu:
        lines.append("\n--- EDUCATION ---")
        for e in edu:
            degree = e.get("degree", "")
            inst = e.get("institution", "")
            dates = f"{e.get('start_date', '')} - {e.get('end_date', '')}"
            lines.append(f"\n{degree} — {inst} | {dates}")
            if e.get("details"):
                lines.append(f"  {e['details']}")

    # Skills
    skills = profile.get("skills", {})
    if any(skills.get(k) for k in ("technical", "soft", "languages", "certifications")):
        lines.append("\n--- SKILLS ---")
        if skills.get("technical"):
            lines.append(f"Technical: {', '.join(skills['technical'])}")
        if skills.get("soft"):
            lines.append(f"Soft: {', '.join(skills['soft'])}")
        if skills.get("languages"):
            lines.append(f"Languages: {', '.join(skills['languages'])}")
        if skills.get("certifications"):
            lines.append(f"Certifications: {', '.join(skills['certifications'])}")

    # Projects
    projects = profile.get("projects", [])
    if projects:
        lines.append("\n--- PROJECTS ---")
        for p in projects:
            lines.append(f"\n{p.get('name', '')} — {p.get('description', '')}")
            if p.get("technologies"):
                lines.append(f"  Tech: {', '.join(p['technologies'])}")
            if p.get("url"):
                lines.append(f"  URL: {p['url']}")

    # Publications
    pubs = profile.get("publications", [])
    if pubs:
        lines.append("\n--- PUBLICATIONS ---")
        for pub in pubs:
            lines.append(f"  - {pub}")

    # Awards
    awards = profile.get("awards", [])
    if awards:
        lines.append("\n--- AWARDS ---")
        for a in awards:
            lines.append(f"  - {a}")

    return "\n".join(lines)


# ── Merge Logic ──────────────────────────────────────────────────────────────
def _merge_list_of_dicts(existing: list[dict], incoming: list[dict], key_fields: list[str]) -> list[dict]:
    """
    Merge two lists of dicts, avoiding duplicates based on key_fields.
    Incoming entries whose key-field values already exist are skipped.
    """
    seen = set()
    for item in existing:
        values = []
        for k in key_fields:
            val = item.get(k, "")
            # Ensure val is a string before calling .strip()
            if not isinstance(val, str):
                val = str(val)
            values.append(val.strip().lower())
        sig = tuple(values)
        seen.add(sig)

    merged = list(existing)
    for item in incoming:
        values = []
        for k in key_fields:
            val = item.get(k, "")
            # Ensure val is a string before calling .strip()
            if not isinstance(val, str):
                val = str(val)
            values.append(val.strip().lower())
        sig = tuple(values)
        if sig not in seen:
            merged.append(item)
            seen.add(sig)
    return merged


def _merge_unique_strings(existing: list[str], incoming: list[str]) -> list[str]:
    """Merge two string lists, keeping unique values (case-insensitive)."""
    def _to_clean_str(s):
        if not isinstance(s, str):
            return str(s).strip().lower()
        return s.strip().lower()

    seen = {_to_clean_str(s) for s in existing}
    merged = list(existing)
    for s in incoming:
        clean_s = _to_clean_str(s)
        if clean_s not in seen:
            merged.append(s)
            seen.add(clean_s)
    return merged


def merge_profiles(existing: dict, new_data: dict, source_file: str = "") -> dict:
    """
    Intelligently merge new_data into existing profile.
    - Personal info: new non-empty values overwrite old empty ones.
    - Lists: merged without duplicates.
    """
    # Personal info — fill blanks, don't overwrite existing values
    for field, value in new_data.get("personal_info", {}).items():
        if value and not existing.get("personal_info", {}).get(field):
            existing.setdefault("personal_info", {})[field] = value

    # Work experience
    existing["work_experience"] = _merge_list_of_dicts(
        existing.get("work_experience", []),
        new_data.get("work_experience", []),
        key_fields=["job_title", "company"],
    )

    # Education
    existing["education"] = _merge_list_of_dicts(
        existing.get("education", []),
        new_data.get("education", []),
        key_fields=["degree", "institution"],
    )

    # Skills
    for category in ("technical", "soft", "languages", "certifications"):
        existing.setdefault("skills", {})[category] = _merge_unique_strings(
            existing.get("skills", {}).get(category, []),
            new_data.get("skills", {}).get(category, []),
        )

    # Projects
    existing["projects"] = _merge_list_of_dicts(
        existing.get("projects", []),
        new_data.get("projects", []),
        key_fields=["name"],
    )

    # Publications & Awards (simple string lists)
    existing["publications"] = _merge_unique_strings(
        existing.get("publications", []),
        new_data.get("publications", []),
    )
    existing["awards"] = _merge_unique_strings(
        existing.get("awards", []),
        new_data.get("awards", []),
    )

    # Metadata
    existing.setdefault("metadata", {})["last_updated"] = datetime.now(timezone.utc).isoformat()
    sources = existing.get("metadata", {}).get("source_files", [])
    if source_file and source_file not in sources:
        sources.append(source_file)
    existing["metadata"]["source_files"] = sources

    return existing


# ── Gemini Extraction ────────────────────────────────────────────────────────
def extract_structured_data(cv_text: str, client, model_name) -> dict:
    """
    Send CV text to Gemini and get back a structured JSON profile.
    """
    schema_json = json.dumps(PROFILE_SCHEMA, indent=2)
    prompt = EXTRACTION_PROMPT.format(schema=schema_json, cv_text=cv_text)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
        }
    )
    
    # The new SDK handles JSON parsing more robustly if response_mime_type is set,
    # but we'll still do a basic check.
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[: raw.rfind("```")]

    try:
        data = json.loads(raw)
        return data
    except json.JSONDecodeError:
        # Fallback if AI wraps it weirdly
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


# ══════════════════════════════════════════════════════════════════════════════
# STANDALONE STREAMLIT UI  (run with: streamlit run oldCVcollector.py)
# ══════════════════════════════════════════════════════════════════════════════
def main():
    st.set_page_config(page_title="CV Profile Manager", layout="wide")
    st.title("🗂️ CV Profile Manager")
    st.caption(
        "Generate your persistent `user_profile.json` by scanning markdown CVs in the `trainingData` folder. "
        "This saves your experience so you don't have to upload CVs every time."
    )

    # ── Sidebar: API Key & Model ─────────────────────────────────────────
    st.sidebar.title("Settings")
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

    available_models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-2.0-flash-thinking-exp"]
    client = None
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            models = client.models.list()
            dynamic = []
            for m in models:
                # The new SDK model object structure is different
                name = m.name
                # Check for generateContent capability if possible, or just gather names
                dynamic.append(name)
            
            if dynamic:
                dynamic.sort(key=lambda x: ("flash" in x.lower() or "pro" in x.lower()), reverse=True)
                available_models = dynamic
        except Exception as e:
            st.sidebar.error(f"Error fetching models: {e}")

    model_name = st.sidebar.selectbox("Select Model", available_models, index=0)

    # ── Current Profile Status ───────────────────────────────────────────
    profile = load_profile()
    has_profile = PROFILE_PATH.exists()

    col_status, col_actions = st.columns([2, 1])
    with col_status:
        if has_profile:
            name = profile.get("personal_info", {}).get("full_name", "Unknown")
            n_jobs = len(profile.get("work_experience", []))
            n_edu = len(profile.get("education", []))
            n_skills = sum(
                len(profile.get("skills", {}).get(k, []))
                for k in ("technical", "soft", "languages", "certifications")
            )
            sources = profile.get("metadata", {}).get("source_files", [])
            last_updated = profile.get("metadata", {}).get("last_updated", "N/A")

            st.success(f"✅ Profile loaded — **{name}**")
            st.markdown(
                f"- **{n_jobs}** work entries · **{n_edu}** education entries · "
                f"**{n_skills}** skills\n"
                f"- Source files: {', '.join(sources) if sources else 'None'}\n"
                f"- Last updated: {last_updated}"
            )
        else:
            st.warning("No profile found. Upload a CV below to get started.")

    with col_actions:
        if has_profile:
            if st.button("🗑️ Reset Profile", use_container_width=True):
                delete_profile()
                st.rerun()

    st.divider()

    # ── Training Data Scan ────────────────────────────────────────────────
    st.subheader("📁 Training Data Scan")
    if not TRAINING_DATA_DIR.exists():
        st.warning(f"Training data directory not found at `{TRAINING_DATA_DIR}`. Creating it...")
        TRAINING_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    md_files = sorted(list(TRAINING_DATA_DIR.glob("*.md")))
    
    if md_files:
        st.info(f"Found **{len(md_files)}** markdown files in `trainingData/`.")
        with st.expander("View found files"):
            for f in md_files:
                st.write(f"- {f.name}")
        
        scan_btn = st.button("� Process all Markdown CVs", use_container_width=True)
        
        if scan_btn:
            if not api_key:
                st.error("Please enter your Gemini API key in the sidebar.")
            else:
                profile = load_profile()
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, f in enumerate(md_files):
                    status_text.text(f"Processing ({i+1}/{len(md_files)}): {f.name}")
                    progress_bar.progress((i + 1) / len(md_files))
                    
                    try:
                        with open(f, "r", encoding="utf-8") as file:
                            cv_text = file.read()
                        
                        if not cv_text.strip():
                            continue
                            
                        extracted = extract_structured_data(cv_text, client, model_name)
                        profile = merge_profiles(profile, extracted, source_file=f.name)
                        st.write(f"✅ Processed {f.name}")
                    except Exception as e:
                        st.error(f"❌ Error processing {f.name}: {e}")
                
                save_profile(profile)
                st.success("💾 Profile updated from training data and saved to `user_profile.json`!")
                st.rerun()
    else:
        st.warning("No markdown files found in `trainingData/`. Please add your `.md` CVs there.")

    st.divider()

    # ── Manual Upload & Extract (Backup) ──────────────────────────────────
    with st.expander("📤 Manual Upload (Backup)"):
        uploads = st.file_uploader(
            "Upload one or more CVs to extract and save your profile data.",
            type=["pdf", "docx", "doc", "md"],
            accept_multiple_files=True,
        )

        extract_btn = st.button("🔍 Extract Uploads & Save", use_container_width=True)

        if extract_btn:
            if not api_key:
                st.error("Please enter your Gemini API key in the sidebar.")
            elif not uploads:
                st.error("Please upload at least one CV file.")
            else:
                profile = load_profile()
                for f in uploads:
                    with st.spinner(f"Extracting text from **{f.name}**..."):
                        if f.name.lower().endswith(".md"):
                            cv_text = f.read().decode("utf-8")
                        else:
                            cv_text = extract_text_from_file(f)

                    if not cv_text.strip():
                        st.warning(f"⚠️ Could not extract text from {f.name}. Skipping.")
                        continue

                    with st.spinner(f"Analysing **{f.name}**..."):
                        try:
                            extracted = extract_structured_data(cv_text, client, model_name)
                            profile = merge_profiles(profile, extracted, source_file=f.name)
                            st.success(f"✅ Extracted data from **{f.name}**")
                        except Exception as e:
                            st.error(f"❌ Error processing {f.name}: {e}")

                save_profile(profile)
                st.success("💾 Profile saved!")
                st.rerun()

    # ── Profile Viewer ───────────────────────────────────────────────────
    if has_profile:
        st.divider()
        st.subheader("👤 Profile Data")

        tab_pretty, tab_raw, tab_text = st.tabs(["Formatted", "Raw JSON", "Plain Text"])

        with tab_pretty:
            pi = profile.get("personal_info", {})
            if pi.get("full_name"):
                st.markdown(f"### {pi['full_name']}")
            info_parts = []
            for key in ("email", "phone", "location", "linkedin", "github", "website"):
                if pi.get(key):
                    info_parts.append(f"**{key.title()}:** {pi[key]}")
            if info_parts:
                st.markdown(" · ".join(info_parts))
            if pi.get("summary"):
                st.markdown(f"*{pi['summary']}*")

            # Work Experience
            work = profile.get("work_experience", [])
            if work:
                st.markdown("---")
                st.markdown("#### 💼 Work Experience")
                for job in work:
                    dates = f"{job.get('start_date', '')} – {job.get('end_date', '')}"
                    st.markdown(f"**{job.get('job_title', '')}** at **{job.get('company', '')}** ({job.get('location', '')})  \n_{dates}_")
                    for r in job.get("responsibilities", []):
                        st.markdown(f"- {r}")
                    for a in job.get("achievements", []):
                        st.markdown(f"- ⭐ {a}")

            # Education
            edu = profile.get("education", [])
            if edu:
                st.markdown("---")
                st.markdown("#### 🎓 Education")
                for e in edu:
                    dates = f"{e.get('start_date', '')} – {e.get('end_date', '')}"
                    st.markdown(f"**{e.get('degree', '')}** — {e.get('institution', '')}  \n_{dates}_")
                    if e.get("details"):
                        st.markdown(f"  {e['details']}")

            # Skills
            skills = profile.get("skills", {})
            if any(skills.get(k) for k in ("technical", "soft", "languages", "certifications")):
                st.markdown("---")
                st.markdown("#### 🛠️ Skills")
                for category in ("technical", "soft", "languages", "certifications"):
                    items = skills.get(category, [])
                    if items:
                        st.markdown(f"**{category.title()}:** {', '.join(items)}")

            # Projects
            projects = profile.get("projects", [])
            if projects:
                st.markdown("---")
                st.markdown("#### 🚀 Projects")
                for p in projects:
                    st.markdown(f"**{p.get('name', '')}** — {p.get('description', '')}")
                    if p.get("technologies"):
                        st.markdown(f"  Tech: {', '.join(p['technologies'])}")

        with tab_raw:
            st.json(profile)

        with tab_text:
            st.text(get_profile_text(profile))

        # ── Manual Edit ──────────────────────────────────────────────────
        st.divider()
        with st.expander("✏️ Manually Edit Profile JSON"):
            edited_json = st.text_area(
                "Edit the JSON below and click Save:",
                value=json.dumps(profile, indent=2, ensure_ascii=False),
                height=400,
            )
            if st.button("💾 Save Manual Edits"):
                try:
                    parsed = json.loads(edited_json)
                    parsed.setdefault("metadata", {})["last_updated"] = datetime.now(timezone.utc).isoformat()
                    save_profile(parsed)
                    st.success("Profile updated!")
                    st.rerun()
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON: {e}")

        # ── Deduplication ────────────────────────────────────────────────
        st.divider()
        st.subheader("🧹 Reduce Profile Duplication")
        st.caption(
            "Uses AI to intelligently merge duplicate work experiences, education, "
            "skills, projects and awards — without losing unique information."
        )

        dedup_btn = st.button("🧹 Deduplicate Profile", use_container_width=True)

        if dedup_btn:
            if not api_key:
                st.error("Please enter your Gemini API key in the sidebar.")
            else:
                with st.spinner("Analysing profile for duplicates..."):
                    try:
                        profile_json = json.dumps(profile, indent=2, ensure_ascii=False)
                        prompt = DEDUPLICATION_PROMPT.format(profile_json=profile_json)

                        response = client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config={
                                'response_mime_type': 'application/json',
                            }
                        )

                        raw = response.text.strip()
                        # Strip markdown fences if present
                        if raw.startswith("```"):
                            raw = raw.split("\n", 1)[1]
                            if raw.endswith("```"):
                                raw = raw[: raw.rfind("```")]

                        deduped = json.loads(raw)

                        # Preserve metadata from original
                        deduped["metadata"] = profile.get("metadata", {})
                        deduped["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()

                        # Show a summary of what changed
                        old_work = len(profile.get("work_experience", []))
                        new_work = len(deduped.get("work_experience", []))
                        old_edu = len(profile.get("education", []))
                        new_edu = len(deduped.get("education", []))
                        old_skills = sum(len(profile.get("skills", {}).get(k, [])) for k in ("technical", "soft", "languages", "certifications"))
                        new_skills = sum(len(deduped.get("skills", {}).get(k, [])) for k in ("technical", "soft", "languages", "certifications"))
                        old_projects = len(profile.get("projects", []))
                        new_projects = len(deduped.get("projects", []))
                        old_awards = len(profile.get("awards", []))
                        new_awards = len(deduped.get("awards", []))

                        st.success("✅ Deduplication complete!")
                        st.markdown(
                            f"| Section | Before | After |\n"
                            f"|---------|--------|-------|\n"
                            f"| Work Experience | {old_work} | {new_work} |\n"
                            f"| Education | {old_edu} | {new_edu} |\n"
                            f"| Skills | {old_skills} | {new_skills} |\n"
                            f"| Projects | {old_projects} | {new_projects} |\n"
                            f"| Awards | {old_awards} | {new_awards} |"
                        )

                        # Show the deduplicated JSON for review before saving
                        with st.expander("📋 Review deduplicated profile", expanded=True):
                            st.json(deduped)

                        # Store in session state so Save button works
                        st.session_state["deduped_profile"] = deduped

                    except json.JSONDecodeError as e:
                        st.error(f"❌ Failed to parse AI response: {e}")
                        st.text(raw)
                    except Exception as e:
                        st.error(f"❌ Deduplication failed: {e}")

        # Save button (outside the if-dedup_btn block so it persists)
        if "deduped_profile" in st.session_state:
            if st.button("💾 Save Deduplicated Profile", use_container_width=True, type="primary"):
                save_profile(st.session_state["deduped_profile"])
                del st.session_state["deduped_profile"]
                st.success("💾 Deduplicated profile saved!")
                st.rerun()


if __name__ == "__main__":
    main()
