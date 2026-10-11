from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class ProcessingStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: str
    video_id: str
    status: str  # pending, running, paused, completed, failed, cancelled
    current_stage: str
    progress_pct: float
    error_message: Optional[str] = None
    retry_count: int
    stage_timings: Dict[str, Any]
    started_at: datetime
    completed_at: Optional[datetime] = None


class ProcessingStartRequest(BaseModel):
    force_restart: bool = False
    whisper_model: Optional[str] = None
    enable_vision: Optional[bool] = None
