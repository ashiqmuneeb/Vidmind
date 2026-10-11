from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class ChapterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    video_id: str
    chapter_index: int
    title: str
    start_time: float
    end_time: float
    summary: Optional[str] = None
    key_topics: List[str] = []
    evidence_segment_ids: List[str] = []


class ChapterListResponse(BaseModel):
    video_id: str
    chapters: List[ChapterResponse]
