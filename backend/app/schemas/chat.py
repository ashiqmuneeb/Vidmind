from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class CitationItem(BaseModel):
    segment_id: Optional[str] = None
    timestamp_start: float
    timestamp_end: float
    excerpt: str
    source_type: str = "transcript"  # transcript, visual_frame, ocr


class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    role: str
    content: str
    question_type: Optional[str] = None
    evidence_citations: List[CitationItem] = []
    confidence_score: float = 1.0
    created_at: datetime
