# 📄 AI CV Tailor & Profile Manager

A suite of local microservices designed to help you manage your professional history and generate perfectly tailored CVs using Google's Gemini AI.

## 🚀 Overview

This project consists of two main components running as Streamlit applications:

1.  **CV Profile Manager (`userCVprofiling.py`)**: 
    - Extracts structured data from your existing CVs (PDF, Word, Markdown).
    - Consolidates and deduplicates your work history, skills, and education.
    - Saves everything to a persistent `user_profile.json` so you never have to upload the same file twice.
2.  **AI CV Tailor (`CV-creator.py`)**:
    - Takes a target Job Description (JD).
    - Uses your saved profile (or new uploads) to draft a tailored CV.
    - Exports the result to high-quality **PDF** and **Word (.docx)**.

---

## 🛠 Features

- **Multi-Format Support**: Parse `.pdf`, `.docx`, `.doc`, and `.md` files.
- **Persistent Profile**: Your data stays local in `user_profile.json`.
- **AI-Powered Deduplication**: Intelligently merge similar roles and skills via Gemini.
- **Interactive Review**: Edit the AI-generated Markdown before exporting.
- **Nginx Reverse Proxy**: Single entry point for both services.

---

## 🏗 Raspberry Pi 4 Deployment

This project is also optimized to run in a containerized environment on a Raspberry Pi 4.

### 1. Prerequisites
Ensure you have Docker and Docker Compose installed on your Pi:
```bash
# Install Docker
curl -sSL https://get.docker.com | sh

# Add your user to the docker group
sudo usermod -aG docker $USER

# Install Docker Compose dependencies
sudo apt-get install -y libffi-dev libssl-dev python3-dev python3 python3-pip
sudo pip3 install docker-compose
```

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

- **CV Tailor**: `http://<your-pi-ip>:8080/cv`
- **Profile Manager**: `http://<your-pi-ip>:8080/profile`

---

## 💻 Local Development (Manual)

If you prefer to run the scripts directly without Docker:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Profile Manager**:
   ```bash
   streamlit run userCVprofiling.py
   ```
3. **Run CV Tailor**:
   ```bash
   streamlit run CV-creator.py
   ```

---

## 📂 Project Structure

- `CV-creator.py`: Main tailoring logic.
- `userCVprofiling.py`: Profile extraction and deduplication logic.
- `trainingData/`: Place your raw Markdown CVs here for bulk scanning.
- `user_profile.json`: Persistent storage for your professional data.
- `docker-compose.yaml`: Service orchestration.
- `nginx.conf`: Routing configuration.

---

## 🔑 Configuration

Both apps require a **Google Gemini API Key**. You can obtain one for free at the [Google AI Studio](https://aistudio.google.com/). Enter the key in the sidebar of the application once it is running.
