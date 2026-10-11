from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from backend.app.db.database import get_db
from backend.app.db.models import TranscriptSegment, Chapter

router = APIRouter(prefix="/videos/{video_id}", tags=["Search"])


class SearchResultItem(BaseModel):
    id: str
    target_type: str  # transcript, chapter, note
    timestamp_start: float
    timestamp_end: float
    text: str
    chapter_title: Optional[str] = None
    score: float = 1.0


class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[SearchResultItem]


@router.get("/search", response_model=SearchResponse)
async def search_video(
    video_id: str,
    q: str = Query(..., min_length=1, description="Query string to search"),
    db: AsyncSession = Depends(get_db)
):
    """Keyword search across transcript segments for a video."""
    query = (
        select(TranscriptSegment)
        .where(
            TranscriptSegment.video_id == video_id,
            TranscriptSegment.text.ilike(f"%{q}%")
        )
        .order_by(TranscriptSegment.start_time)
        .limit(30)
    )
    res = await db.execute(query)
    segments = res.scalars().all()

    items = [
        SearchResultItem(
            id=s.id,
            target_type="transcript",
            timestamp_start=s.start_time,
            timestamp_end=s.end_time,
            text=s.text,
            score=1.0
        )
        for s in segments
    ]

    return SearchResponse(query=q, total=len(items), results=items)
