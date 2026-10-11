# VidMind Configuration Reference

All settings are configured through environment variables or a `.env` file in the project root.

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `APP_NAME` | `VidMind` | Application name displayed in API & UI |
| `DEBUG` | `true` | Enables detailed logging and debug endpoints |
| `HOST` | `0.0.0.0` | Bind IP for the FastAPI application |
| `PORT` | `8000` | Port for backend REST API |
| `DATABASE_URL` | `sqlite+aiosqlite:///./data/vidmind.db` | SQLAlchemy connection string |
| `DATA_DIRECTORY` | `./data` | Filesystem root for media, frames, transcripts, and vectors |
| `HARDWARE_PROFILE` | `auto` | `auto`, `low` (CPU int8), `medium`, `high` (CUDA FP16) |
| `TRANSCRIPTION_MODEL` | `base` | `tiny`, `base`, `small`, `medium`, `large-v3` |
| `TRANSCRIPTION_DEVICE`| `cpu` | `cpu` or `cuda` |
| `TRANSCRIPTION_COMPUTE_TYPE` | `int8` | `int8`, `float16`, `float32` |
| `TRANSCRIPTION_CPU_THREADS` | `3` | Number of worker threads for Whisper CPU inference |
| `TRANSCRIPTION_VAD_FILTER` | `true` | Voice Activity Detection to skip non-speech regions |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434`| Endpoint for local Ollama server |
| `OLLAMA_MODEL` | `llama3.2:1b` | Default Ollama model name |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model for semantic search |
| `CHUNK_TARGET_MINUTES`| `10` | Target duration for semantic speech chunking |
| `CHUNK_MIN_MINUTES` | `5` | Minimum chunk boundary |
| `CHUNK_MAX_MINUTES` | `15` | Maximum chunk boundary |
| `ENABLE_VISION` | `false` | Enable visual frame extraction and slide OCR |
| `ENABLE_OCR` | `false` | Enable optical character recognition on slides |
| `MAX_CONCURRENT_JOBS` | `2` | Maximum background processing jobs running simultaneously |
