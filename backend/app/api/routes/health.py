import os
import shutil
import psutil
import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.app.core.config import settings
from backend.app.db.database import get_db

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])


@router.get("")
async def get_health_status(db: AsyncSession = Depends(get_db)):
    """Comprehensive health and hardware diagnostic check."""
    # 1. Test Database
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    # 2. Hardware metrics
    cpu_count = os.cpu_count() or 2
    mem = psutil.virtual_memory() if hasattr(psutil, "virtual_memory") else None
    mem_total_gb = round(mem.total / (1024**3), 2) if mem else 8.0
    mem_free_gb = round(mem.available / (1024**3), 2) if mem else 1.0

    # 3. Disk Space
    disk = shutil.disk_usage(settings.DATA_DIRECTORY)
    disk_free_gb = round(disk.free / (1024**3), 2)

    # 4. Check CUDA
    cuda_available = False
    cuda_device = None
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            cuda_device = torch.cuda.get_device_name(0)
    except ImportError:
        pass

    # 5. Check Ollama server availability
    ollama_active = False
    try:
        async with httpx.AsyncClient(timeout=1.5) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                ollama_active = True
    except Exception:
        ollama_active = False

    # 6. Check FFmpeg in PATH
    ffmpeg_available = bool(shutil.which("ffmpeg"))

    # Determine recommended profile
    recommended_profile = "low"
    recommended_whisper = "base"
    if cuda_available:
        recommended_profile = "high"
        recommended_whisper = "large-v3"
    elif cpu_count >= 8 and mem_total_gb >= 16:
        recommended_profile = "medium"
        recommended_whisper = "small"

    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "storage": {
            "data_directory": settings.DATA_DIRECTORY,
            "free_space_gb": disk_free_gb,
        },
        "hardware": {
            "profile": recommended_profile,
            "cpu_logical_cores": cpu_count,
            "memory_total_gb": mem_total_gb,
            "memory_available_gb": mem_free_gb,
            "cuda_available": cuda_available,
            "cuda_device": cuda_device,
            "ffmpeg_available": ffmpeg_available,
        },
        "ai_providers": {
            "whisper_model": settings.TRANSCRIPTION_MODEL,
            "whisper_device": settings.TRANSCRIPTION_DEVICE,
            "whisper_compute_type": settings.TRANSCRIPTION_COMPUTE_TYPE,
            "recommended_whisper": recommended_whisper,
            "ollama_base_url": settings.OLLAMA_BASE_URL,
            "ollama_active": ollama_active,
            "ollama_model": settings.OLLAMA_MODEL,
            "embedding_model": settings.EMBEDDING_MODEL,
        },
    }
