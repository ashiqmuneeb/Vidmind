import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from backend.app.db.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Video(Base):
    __tablename__ = "videos"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    channel = Column(String(255), nullable=True)
    duration_seconds = Column(Float, default=0.0)
    source_type = Column(String(50), default="youtube")  # youtube, upload, local
    source_url = Column(String(1000), nullable=True)
    file_path = Column(String(1000), nullable=True)
    audio_path = Column(String(1000), nullable=True)
    thumbnail_url = Column(String(1000), nullable=True)
    metadata_json = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    jobs = relationship("ProcessingJob", back_populates="video", cascade="all, delete-orphan")
    segments = relationship("TranscriptSegment", back_populates="video", cascade="all, delete-orphan")
    chunks = relationship("SemanticChunk", back_populates="video", cascade="all, delete-orphan")
    chapters = relationship("Chapter", back_populates="video", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="video", cascade="all, delete-orphan")
    visual_frames = relationship("VisualFrame", back_populates="video", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="video", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="video", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="video", cascade="all, delete-orphan")
    feedback = relationship("UserFeedback", back_populates="video", cascade="all, delete-orphan")


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    
    # State tracking: pending, running, paused, completed, failed, cancelled
    status = Column(String(50), default="pending", index=True)
    # Stages: VALIDATE, SUBTITLE_CHECK, AUDIO_EXTRACT, TRANSCRIBE, QC, CHUNK, CHAPTERS, VISUAL, EMBED, SUMMARIZE, NOTES, COMPLETE
    current_stage = Column(String(50), default="VALIDATE")
    progress_pct = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    config_json = Column(JSON, default=dict)
    stage_timings_json = Column(JSON, default=dict)
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    video = relationship("Video", back_populates="jobs")


class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    segment_index = Column(Integer, nullable=False)
    
    start_time = Column(Float, nullable=False, index=True)
    end_time = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    confidence = Column(Float, default=1.0)
    speaker = Column(String(100), nullable=True)
    source = Column(String(50), default="whisper")  # whisper, subtitle, manual
    
    is_flagged_qc = Column(Boolean, default=False)
    qc_flags_json = Column(JSON, default=list)

    video = relationship("Video", back_populates="segments")

    __table_args__ = (
        Index("idx_seg_video_time", "video_id", "start_time"),
        Index("idx_seg_video_index", "video_id", "segment_index"),
    )


class SemanticChunk(Base):
    __tablename__ = "semantic_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    
    key_points_json = Column(JSON, default=list)
    concepts_json = Column(JSON, default=list)
    claims_json = Column(JSON, default=list)
    evidence_segment_ids = Column(JSON, default=list)

    video = relationship("Video", back_populates="chunks")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    chapter_index = Column(Integer, nullable=False)
    
    title = Column(String(255), nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    summary = Column(Text, nullable=True)
    key_topics_json = Column(JSON, default=list)
    evidence_segment_ids = Column(JSON, default=list)

    video = relationship("Video", back_populates="chapters")


class VisualFrame(Base):
    __tablename__ = "visual_frames"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(Float, nullable=False)
    frame_path = Column(String(1000), nullable=False)
    ocr_text = Column(Text, nullable=True)
    visual_description = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)
    associated_segment_id = Column(String(36), nullable=True)

    video = relationship("Video", back_populates="visual_frames")


class EmbeddingRecord(Base):
    __tablename__ = "embedding_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    target_type = Column(String(50), nullable=False)  # segment, chunk, chapter, visual
    target_id = Column(String(36), nullable=False)
    text_content = Column(Text, nullable=False)
    vector_id = Column(Integer, nullable=True)
    metadata_json = Column(JSON, default=dict)


class Note(Base):
    __tablename__ = "notes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    style = Column(String(50), default="standard")  # standard, concise, detailed, academic, cornell, cheat_sheet
    title = Column(String(255), default="Video Notes")
    markdown_content = Column(Text, nullable=False)
    structured_json = Column(JSON, default=dict)
    is_user_edited = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    video = relationship("Video", back_populates="notes")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=True)
    evidence_citations_json = Column(JSON, default=list)
    confidence_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    timestamp_start = Column(Float, nullable=True)
    timestamp_end = Column(Float, nullable=True)
    concept_tag = Column(String(100), nullable=True)

    video = relationship("Video", back_populates="flashcards")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), default="Knowledge Check")
    questions_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="quizzes")


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    target_type = Column(String(50), nullable=False)  # message, note, segment
    target_id = Column(String(36), nullable=False)
    feedback_type = Column(String(50), nullable=False)  # wrong, hallucination, bad_timestamp, useful
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="feedback")
