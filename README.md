# VidMind — AI Long-Video Transcription, Understanding, Notes & Q&A Platform

> **VidMind** transforms long-form videos (including 10+ hour lectures, conferences, and courses) into evidence-grounded timestamped transcripts, hierarchical summaries, topic chapters, customizable study notes, quizzes, flashcards, and an interactive conversational assistant with clickable citations.

---

## Key Capabilities

- **10+ Hour Video Processing**: Streamed chunking and bounded memory processing prevents RAM crashes.
- **Resumable State Machine**: Automatic checkpoints at each stage (`INGEST` → `TRANSCRIBE` → `QC` → `CHUNK` → `CHAPTER` → `EMBED` → `NOTES`). If interrupted, processing resumes seamlessly.
- **Evidence-First Grounding**: Every answer, note, and quiz links to verifiable segment timestamps `[HH:MM:SS]`.
- **Hallucination Prevention**: Explicit uncertainty handling (*"Not enough evidence in the video to answer this confidently"*).
- **Multi-Style Notes**: Generate standard, Cornell, concise, academic, tutorial, and cheat sheet notes.
- **Interactive 3-Panel Workspace**: Synchronized video playback with chapter timeline, transcript explorer, and AI assistant.
- **Zero-Cloud Local Privacy**: All media, transcripts, and LLM processing remain on your local machine by default.

---

## Hardware Requirements

| Tier | Specs | Whisper Model | LLM Recommendation |
| :--- | :--- | :--- | :--- |
| **Low / CPU-Only** *(Current host)* | 2-4 CPU Cores, 8 GB RAM, No GPU | `base` / `small` (`int8`) | Ollama `llama3.2:1b` / Fallback |
| **Medium** | 6-8 CPU Cores or 6GB GPU, 16 GB RAM | `small` / `medium` | Ollama `llama3.2:3b` |
| **High** | NVIDIA GPU (12GB+ VRAM), 32 GB RAM | `large-v3` (`float16`) | Ollama `llama3.1:8b` / `qwen2.5:7b` |

---

## Quickstart Guide

### 1. Prerequisites
Ensure **FFmpeg** and **Node.js 18+** are installed.
- Windows: `choco install ffmpeg` or `winget install Gyan.FFmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### 2. Environment Setup (Conda)
```powershell
# Create environment
conda create -n vidmind python=3.11 -y
conda activate vidmind

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3. Verify Dependencies
```powershell
python scripts/check_dependencies.py
```

### 4. Optional: Start Local LLM (Ollama)
```powershell
ollama run llama3.2:1b
```

### 5. Launch Full Stack
```powershell
.\scripts\run_dev.ps1
```
The web application is live at `http://localhost:5173` and the backend Swagger API at `http://localhost:8000/docs`.

---

## Testing & Accuracy Evaluation

```powershell
# Run backend test suite
pytest backend/tests/ -v

# Run golden dataset grounding benchmark
pytest backend/tests/evaluation/ -v
```

---

## Documentation Links
- [System Architecture](docs/architecture.md)
- [Installation Guide](docs/installation.md)
- [Configuration Reference](docs/configuration.md)
- [API Reference](docs/api.md)
- [AI Processing Pipeline](docs/ai-pipeline.md)
- [Accuracy & Evaluation](docs/accuracy.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Developer Guide](docs/development.md)

---

## License
MIT License. See [LICENSE](LICENSE) for details.
