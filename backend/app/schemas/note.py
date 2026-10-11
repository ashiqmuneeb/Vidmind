from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    video_id: str
    style: str
    title: str
    markdown_content: str
    structured_json: Dict[str, Any]
    is_user_edited: bool
    created_at: datetime
    updated_at: datetime


class NoteUpdateRequest(BaseModel):
    markdown_content: str
    title: Optional[str] = None


class NoteGenerateRequest(BaseModel):
    style: str = "standard"  # standard, concise, detailed, academic, cornell, cheat_sheet
    custom_instructions: Optional[str] = None
