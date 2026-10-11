# VidMind REST API Reference

The backend provides a comprehensive RESTful API built on FastAPI with interactive Swagger documentation at `/docs` and ReDoc at `/redoc`.

---

## 1. System Endpoints

### `GET /api/health`
Returns system status, hardware diagnostics, and component health.
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "hardware": {
    "profile": "low",
    "cpu_count": 4,
    "cuda_available": false
  },
  "database": "connected"
}
```

---

## 2. Videos & Ingestion

### `GET /api/videos`
Lists all ingested videos with pagination, search, and status filtering.

### `POST /api/videos`
Registers a new YouTube URL or uploaded file for processing.
**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "title_override": null,
  "enable_vision": false
}
```

### `GET /api/videos/{id}`
Returns video details, metadata, duration, and processing status.

### `DELETE /api/videos/{id}`
Deletes video and purges associated media, transcript, and vector indexes.

---

## 3. Processing Pipeline

### `POST /api/videos/{id}/process`
Initiates or resumes the multi-stage background processing pipeline.

### `GET /api/videos/{id}/processing`
Returns real-time processing progress, current stage, percent complete, and stage timings.

---

## 4. Transcripts & Chapters

### `GET /api/videos/{id}/transcript`
Returns timestamped transcript segments with speaker tags and quality control flags.

### `GET /api/videos/{id}/chapters`
Returns detected topic chapters grounded in transcript evidence.

---

## 5. Notes & Study Tools

### `GET /api/videos/{id}/notes`
Returns generated notes in the specified style (`standard`, `concise`, `detailed`, `academic`, `cornell`).

### `PUT /api/videos/{id}/notes`
Updates or customizes user notes.

### `POST /api/videos/{id}/flashcards`
Generates grounded study flashcards with source timestamps.

### `POST /api/videos/{id}/quiz`
Generates an interactive multiple-choice and conceptual quiz.

---

## 6. Grounded AI Chat & Search

### `POST /api/videos/{id}/chat`
Asks a question about the video with strict grounding and timestamp citations.
**Request Body:**
```json
{
  "message": "What did the speaker say about gradient descent?",
  "session_id": "optional-uuid"
}
```
**Response Body:**
```json
{
  "answer": "The speaker explains that gradient descent updates parameters...",
  "evidence": [
    {
      "segment_id": "seg-104",
      "timestamp_start": 5072.0,
      "timestamp_end": 5110.0,
      "text": "..."
    }
  ],
  "confidence": 0.94
}
```

### `POST /api/videos/{id}/search`
Hybrid vector + BM25 keyword search across transcript segments, visual frames, and summaries.

---

## 7. Export

### `GET /api/videos/{id}/export/{format}`
Exports video notes and transcripts in `markdown`, `txt`, `json`, `srt`, `vtt`, or `pdf`.
