# VidMind Architecture & System Design

VidMind is a production-grade AI platform for long-video transcription, comprehension, structured note generation, and conversational question-answering with timestamped citations.

## 1. High-Level Architectural Diagram

```mermaid
flowchart TD
    subgraph Client ["Client Layer"]
        Web[React + Vite Single-Page Application]
        Player[HTML5 Video Player / YouTube Embed]
        ChatUI[Interactive Grounded Q&A]
        NotesUI[Multi-Style Note Editor]
    end

    subgraph API ["FastAPI Gateway (:8000)"]
        Routes[REST API Endpoints]
        Dep[Dependency Injection & Auth]
        Validation[Pydantic v2 Schema Validation]
    end

    subgraph CoreEngine ["Core Processing & AI Engine"]
        JobRunner[Asynchronous Resumable Job State Machine]
        YTExtractor[yt-dlp Metadata & Stream Extractor]
        AudioProc[FFmpeg Audio Normalizer & Slicer]
        WhisperSTT[faster-whisper Engine (CPU int8)]
        QualityControl[Transcript QC & Hallucination Filter]
        SemanticChunker[Semantic & Temporal Chunking Engine]
        ChapterDetector[Topic & Chapter Boundary Detector]
        VisionOCR[FFmpeg Frame Extractor + OCR]
        VectorEngine[FAISS Vector Store + BM25 Hybrid Retriever]
        LLMOrchestrator[Ollama Local LLM Provider with Strict Grounding]
        NoteGen[Hierarchical & Multi-Style Note Generator]
    end

    subgraph Persistence ["Persistence Layer"]
        SQLite[(SQLite with WAL Mode / PostgreSQL)]
        VectorIndex[(FAISS Binary Index)]
        FileStore[(Local Media & Cache Store /data)]
    end

    Web --> Routes
    Routes --> JobRunner
    JobRunner --> CoreEngine
    CoreEngine --> Persistence
```

## 2. Core Subsystems

### 2.1 Video Ingestion Subsystem
- **Metadata Probing**: Rapid extraction of title, channel, duration, and thumbnail without downloading high-resolution video streams upfront.
- **Subtitle-First Strategy**: If human-verified or platform subtitles are detected and enabled, they are extracted directly to bypass initial compute overhead, with an optional Whisper cross-check.
- **Audio Extraction**: FFmpeg extracts 16kHz mono audio (16-bit PCM WAV/FLAC) with two-pass loudness normalization (`loudnorm`).

### 2.2 Streaming Transcription Subsystem
- **Engine**: `faster-whisper` based on CTranslate2.
- **Low-Tier Hardware Adaptation**: Runs with `device="cpu"`, `compute_type="int8"`, and 3 worker threads to respect dual-core host hardware.
- **Checkpointing**: Ingests transcripts in incremental batches into the database. If interrupted, the job resumes from the last transcribed timestamp without reprocessing.

### 2.3 Transcript Quality Control Engine
- Flags repetitive acoustic hallucinations (common in Whisper on long silences/music).
- Identifies unusually long/short segments, high-perplexity phrases, and broken sentence boundaries.

### 2.4 Semantic Chunking & Chaptering
- Partitions continuous speech into 5-to-15 minute cohesive semantic units.
- Evaluates pause boundaries, sentence terminal punctuation, and topic transitions.
- Each chunk maintains a list of source segment IDs for rigorous provenance tracking.

### 2.5 Hybrid Vector & Keyword Retrieval (RAG)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` produces 384-dimensional dense vectors with minimal CPU footprint.
- **FAISS**: Local flat L2/Cosine index stored on disk.
- **BM25**: Keyword search over raw transcript segments, visual OCR text, and summaries.
- **Reciprocal Rank Fusion (RRF)**: Merges dense and sparse rankings to ensure zero keyword misses while maintaining conceptual breadth.

### 2.6 Grounded Question-Answering & Hallucination Defense
- **Rule 1 Enforcement**: If retrieved evidence score is below threshold, replies: *"Not enough evidence in the video to answer this confidently."*
- **Clickable Citations**: Every factual claim is decorated with `[HH:MM:SS]` timestamps linked directly to the video player timeline.

### 2.7 Multi-Style Note Engine
- Supports standard, concise, academic, Cornell, tutorial, cheat sheet, and custom user prompts.
- Generates structured Markdown and JSON trees linking concepts directly to video chapters.
