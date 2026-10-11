from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.db.database import get_db
from backend.app.db.models import Video, TranscriptSegment, Chapter
from backend.app.schemas.transcript import TranscriptResponse, TranscriptSegmentResponse
from backend.app.schemas.chapter import ChapterListResponse, ChapterResponse

router = APIRouter(prefix="/videos/{video_id}", tags=["Transcripts & Chapters"])


@router.get("/transcript", response_model=TranscriptResponse)
async def get_transcript(
    video_id: str,
    search: Optional[str] = Query(None, description="Search term in transcript text"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve all timestamped transcript segments for a video."""
    v_res = await db.execute(select(Video).where(Video.id == video_id))
    video = v_res.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found.")

    query = select(TranscriptSegment).where(TranscriptSegment.video_id == video_id)
    if search:
        query = query.where(TranscriptSegment.text.ilike(f"%{search}%"))
    query = query.order_by(TranscriptSegment.segment_index)

    result = await db.execute(query)
    segments = result.scalars().all()

    return TranscriptResponse(
        video_id=video_id,
        total_segments=len(segments),
        duration_seconds=video.duration_seconds,
        segments=[TranscriptSegmentResponse.model_validate(s) for s in segments]
    )


@router.get("/chapters", response_model=ChapterListResponse)
async def get_chapters(
    video_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve grounded chapters for a video."""
    query = select(Chapter).where(Chapter.video_id == video_id).order_by(Chapter.chapter_index)
    result = await db.execute(query)
    chapters = result.scalars().all()

    return ChapterListResponse(
        video_id=video_id,
        chapters=[ChapterResponse.model_validate(c) for c in chapters]
    )
