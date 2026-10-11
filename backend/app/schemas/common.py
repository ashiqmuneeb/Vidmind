from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[str] = None


class HardwareInfo(BaseModel):
    profile: str
    cpu_count: int
    cuda_available: bool
    cuda_device_name: Optional[str] = None
    whisper_recommended_model: str
    ollama_status: str
