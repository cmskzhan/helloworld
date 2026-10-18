# 📄 AI CV Tailor & Profile Manager

A suite of local microservices designed to help you manage your professional history and generate perfectly tailored CVs using Google's Gemini AI. Designed for low resource usage on Raspberry Pi using FastAPI and vanilla JS/HTML.

## 🚀 Overview

This project consists of two main components served by a single FastAPI backend:

1.  **CV Profile Manager**: 
    - Extracts structured data from your existing CVs (PDF, Word, Markdown).
    - Consolidates and deduplicates your work history, skills, and education.
    - Saves everything to a persistent `user_profile.json` so you never have to upload the same file twice.
2.  **AI CV Tailor**:
    - Takes a target Job Description (JD).
    - Uses your saved profile (or new uploads) to draft a tailored CV.
    - Exports the result to high-quality **PDF** and **Word (.docx)**.

---

## 🛠 Features

- **Multi-Format Support**: Parse `.pdf`, `.docx`, `.doc`, and `.md` files.
- **Persistent Profile**: Your data stays local in `user_profile.json`.
- **AI-Powered Deduplication**: Intelligently merge similar roles and skills via Gemini.
- **Interactive Review**: Edit the AI-generated Markdown before exporting.
- **High Performance UI**: Built with vanilla HTML/JS/CSS to minimize memory usage on RPi (compared to Streamlit).

---

## 🏗 Raspberry Pi 4 Deployment

This project is optimized to run in a containerized environment on a Raspberry Pi 4. The transition from Streamlit to FastAPI + static HTML drastically reduces idle RAM usage and improves load times.

### 1. Prerequisites
Ensure you have Docker and Docker Compose installed on your Pi:

### 2. Build the Containers
Navigate to the project directory and build the images:
```bash
cd ~/github/helloworld/concepts/CV-creator
docker compose build
```
*Note: The first build might take a few minutes as it installs Python dependencies.*

### 3. Start the Services
Run the containers in detached mode:
```bash
docker compose up -d
```

### 4. Access the Applications
Once the containers are running, you can access the tools via your Pi's IP address on port **8080**:

- **CV Tailor**: `http://<your-pi-ip>:8080/index.html`
- **Profile Manager**: `http://<your-pi-ip>:8080/profile.html`

---

## 💻 Local Development (Manual)

If you prefer to run the scripts directly without Docker:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Backend App**:
   ```bash
   uvicorn main:app --reload
   ```
3. **Access Apps**: Navigate to `http://localhost:8000/`

---

## 📂 Project Structure

- `main.py`: Main FastAPI application handling all API routes.
- `core_profiling.py`, `core_cv.py`: Backend business logic for AI extraction and PDF/DOCX generation.
- `static/`: HTML, JS, and CSS files serving the user interface.
- `trainingData/`: Place your raw Markdown CVs here for bulk scanning.
- `user_profile.json`: Persistent storage for your professional data.
- `docker-compose.yaml`: Service orchestration linking backend and Nginx.
- `nginx.conf`: Nginx routing configuration for static files and reverse proxy API.

---

## 🔑 Configuration

Both apps require a **Google Gemini API Key**. You can obtain one for free at the Google AI Studio. Enter the key in the settings panel of the application once it is running.
