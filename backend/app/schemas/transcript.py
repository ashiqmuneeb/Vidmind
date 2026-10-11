from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class TranscriptSegmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    video_id: str
    segment_index: int
    start_time: float
    end_time: float
    text: str
    language: str
    confidence: float
    speaker: Optional[str] = None
    source: str
    is_flagged_qc: bool
    qc_flags_json: List[str]


class TranscriptResponse(BaseModel):
    video_id: str
    total_segments: int
    duration_seconds: float
    segments: List[TranscriptSegmentResponse]
