# VidMind Installation & Environment Setup Guide

VidMind supports cross-platform execution on Windows, macOS, and Linux. This guide covers setup from source using Conda or standard Python virtual environments.

---

## 1. Prerequisites

### 1.1 Hardware Recommendations
* **Minimum**: 2 CPU cores, 8 GB RAM, 10 GB free disk space.
* **Recommended**: 4+ CPU cores (or NVIDIA CUDA GPU with 6GB+ VRAM), 16 GB RAM, SSD storage.

### 1.2 System Dependencies
* **FFmpeg 6+**: Required for media ingestion, audio splitting, and frame extraction.
  * *Windows*: `choco install ffmpeg` or `winget install Gyan.FFmpeg`
  * *macOS*: `brew install ffmpeg`
  * *Linux (Ubuntu/Debian)*: `sudo apt update && sudo apt install -y ffmpeg`
* **Node.js (v18+) & npm**: Required for building and running the React/Vite frontend.
* **Ollama (Optional for local LLM)**: Download from [ollama.com](https://ollama.com).

---

## 2. Windows Installation (Recommended Flow)

### Step 1: Create & Activate Conda Environment
```powershell
# Using Conda
conda create -n vidmind python=3.11 -y
conda activate vidmind

# Or automated PowerShell setup
.\scripts\setup_environment.ps1
```

### Step 2: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies
```powershell
cd frontend
npm install
cd ..
```

### Step 4: Verify Environment
```powershell
python scripts/check_dependencies.py
```

### Step 5: Initialize Database
```powershell
python scripts/init_database.py
```

---

## 3. macOS & Linux Installation

```bash
# 1. Clone repository
git clone https://github.com/your-org/vidmind.git
cd vidmind

# 2. Create conda environment
conda env create -f environment.yml
conda activate vidmind

# 3. Verify dependencies
python scripts/check_dependencies.py

# 4. Initialize Database
python scripts/init_database.py

# 5. Install frontend packages
cd frontend && npm install && cd ..
```

---

## 4. Setting up Local LLM (Ollama)

1. Start Ollama:
   ```bash
   ollama serve
   ```
2. Pull recommended lightweight model:
   ```bash
   ollama pull llama3.2:1b
   # Or for larger systems:
   ollama pull llama3.2:3b
   ```
3. Configure `OLLAMA_MODEL` and `OLLAMA_BASE_URL` in `.env`.

---

## 5. Starting Development Servers

Run backend and frontend simultaneously:
```powershell
# Windows PowerShell
.\scripts\run_dev.ps1

# Or run separately:
# Terminal 1 (Backend):
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 (Frontend):
cd frontend && npm run dev
```

Access the UI at `http://localhost:5173` and API documentation at `http://localhost:8000/docs`.
