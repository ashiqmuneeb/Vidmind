from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.app.db.database import get_db
from backend.app.db.models import Video, ProcessingJob
from backend.app.schemas.video import VideoCreateRequest, VideoResponse, VideoListResponse
from backend.app.core.security import is_valid_youtube_url, sanitize_filename
from backend.app.core.logging import logger

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.get("", response_model=VideoListResponse)
async def list_videos(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve all registered videos ordered by creation date."""
    query = select(Video).order_by(desc(Video.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    videos = result.scalars().all()
    
    # Count total
    count_query = select(Video)
    count_res = await db.execute(count_query)
    total = len(count_res.scalars().all())

    return VideoListResponse(
        videos=[VideoResponse.model_validate(v) for v in videos],
        total=total
    )


@router.post("", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def create_video(
    payload: VideoCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Register a new YouTube URL or local file to VidMind."""
    if not payload.url and not payload.title:
        raise HTTPException(status_code=400, detail="Must provide either a URL or a title.")

    source_type = "youtube" if payload.url and is_valid_youtube_url(payload.url) else "local"
    title = payload.title or ("YouTube Video" if source_type == "youtube" else "Uploaded Video")

    video = Video(
        title=title,
        source_url=payload.url,
        source_type=source_type,
        metadata_json={
            "enable_vision": payload.enable_vision,
            "enable_ocr": payload.enable_ocr,
        }
    )
    db.add(video)
    await db.flush()

    # Automatically create initial processing job in pending state
    job = ProcessingJob(
        video_id=video.id,
        status="pending",
        current_stage="VALIDATE",
        progress_pct=0.0
    )
    db.add(job)
    await db.commit()
    await db.refresh(video)

    logger.info(f"Registered new video: {video.id} ({video.title})")
    return VideoResponse.model_validate(video)


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get single video details by ID."""
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found.")
    return VideoResponse.model_validate(video)


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(
    video_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a video and all associated transcripts, notes, and jobs."""
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found.")
    
    await db.delete(video)
    await db.commit()
    logger.info(f"Deleted video {video_id} and associated artifacts.")
    return None
