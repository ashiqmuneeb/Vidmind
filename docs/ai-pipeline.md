# VidMind AI Processing Pipeline

VidMind breaks down the complexity of long-form audio/video analysis into 12 idempotent, resumable stages.

---

## 1. Pipeline Stages

```
STAGE 1: Ingest & Metadata Validation
  ↓
STAGE 2: Subtitle Probing (Human / Auto subtitles)
  ↓
STAGE 3: Audio Extraction & Loudness Normalization (FFmpeg 16kHz mono)
  ↓
STAGE 4: Chunked Speech-to-Text Transcription (faster-whisper CPU int8)
  ↓
STAGE 5: Quality Control & Hallucination Filtering
  ↓
STAGE 6: Semantic Chunking (5–15 min natural boundary partitioning)
  ↓
STAGE 7: Grounded Topic & Chapter Detection
  ↓
STAGE 8: Visual Frame & Slide OCR Analysis (Optional)
  ↓
STAGE 9: Knowledge & Entity Extraction
  ↓
STAGE 10: Hierarchical Summarization (Chunk → Chapter → Global)
  ↓
STAGE 11: Hybrid Vector (FAISS) + BM25 Search Indexing
  ↓
STAGE 12: Study Guide, Flashcard & Quiz Artifact Generation
```

---

## 2. Long-Video (10+ Hour) Handling Architecture

1. **Bounded Memory Invariant**: Audio files are processed in streamed 15-minute windows or decoded via CTranslate2 generator streams. Raw uncompressed audio is never accumulated in memory.
2. **Persistent Checkpointing**: After every batch of transcript segments or semantic chunks, records and execution states are committed to SQLite. If the process is halted or machine reboots, processing resumes from the last completed checkpoint.
3. **Hierarchical Summarization**: Summaries are generated bottom-up:
   * Level 1: Semantic Chunk Summary (from transcript segments)
   * Level 2: Chapter Summary (synthesized from chunk summaries)
   * Level 3: Global Executive Summary (synthesized from chapter summaries)
   * *This ensures the LLM context window is never overloaded, regardless of video length.*
