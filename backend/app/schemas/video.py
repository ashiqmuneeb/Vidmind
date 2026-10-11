from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class VideoCreateRequest(BaseModel):
    url: Optional[str] = Field(None, description="YouTube or direct media URL")
    title: Optional[str] = Field(None, description="Optional custom title")
    enable_vision: bool = Field(False, description="Whether to extract video frames & run OCR")
    enable_ocr: bool = Field(False, description="Whether to extract text via OCR")


class VideoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: Optional[str] = None
    channel: Optional[str] = None
    duration_seconds: float
    source_type: str
    source_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    metadata_json: Optional[Dict[str, Any]] = None


class VideoListResponse(BaseModel):
    videos: List[VideoResponse]
    total: int
