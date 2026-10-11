# VidMind Troubleshooting & Diagnostics

## 1. Common Issues & Resolutions

### Issue: "FFmpeg not found in PATH"
- **Cause**: Audio extraction and frame generation require FFmpeg on the system PATH.
- **Fix**:
  - Run `choco install ffmpeg` on Windows or install via `winget install Gyan.FFmpeg`.
  - Verify in terminal with `ffmpeg -version`.

### Issue: "Ollama connection refused on http://127.0.0.1:11434"
- **Cause**: The Ollama daemon is not running or model not pulled.
- **Fix**:
  - Run `ollama serve` in a background terminal.
  - Pull model: `ollama pull llama3.2:1b`.
  - If Ollama is unavailable, VidMind automatically switches to its deterministic fallback provider for study summaries and testing.

### Issue: "Out of Memory (OOM) during Whisper transcription"
- **Cause**: Whisper model size is too large for host RAM.
- **Fix**:
  - Check `.env` and set `TRANSCRIPTION_MODEL=base` or `TRANSCRIPTION_MODEL=tiny`.
  - Set `TRANSCRIPTION_COMPUTE_TYPE=int8`.

### Issue: "CORS errors in browser console"
- **Cause**: Frontend origin not permitted by FastAPI backend.
- **Fix**:
  - Add frontend port (e.g., `http://localhost:5173`) to `CORS_ORIGINS` in `.env`.
