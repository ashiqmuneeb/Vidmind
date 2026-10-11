from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.app.db.database import get_db
from backend.app.db.models import Video, ProcessingJob
from backend.app.schemas.processing import ProcessingStatusResponse, ProcessingStartRequest
from backend.app.core.logging import logger

router = APIRouter(prefix="/videos/{video_id}", tags=["Processing"])


@router.get("/processing", response_model=ProcessingStatusResponse)
async def get_processing_status(
    video_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get the current or latest processing job status for a video."""
    query = (
        select(ProcessingJob)
        .where(ProcessingJob.video_id == video_id)
        .order_by(desc(ProcessingJob.started_at))
        .limit(1)
    )
    result = await db.execute(query)
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="No processing job found for this video.")

    return ProcessingStatusResponse(
        job_id=job.id,
        video_id=job.video_id,
        status=job.status,
        current_stage=job.current_stage,
        progress_pct=job.progress_pct,
        error_message=job.error_message,
        retry_count=job.retry_count,
        stage_timings=job.stage_timings_json or {},
        started_at=job.started_at,
        completed_at=job.completed_at
    )


@router.post("/process", response_model=ProcessingStatusResponse)
async def start_processing(
    video_id: str,
    payload: ProcessingStartRequest = ProcessingStartRequest(),
    db: AsyncSession = Depends(get_db)
):
    """Trigger or resume background processing for a video."""
    # Verify video exists
    v_res = await db.execute(select(Video).where(Video.id == video_id))
    video = v_res.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found.")

    # Find latest job or create new one
    query = (
        select(ProcessingJob)
        .where(ProcessingJob.video_id == video_id)
        .order_by(desc(ProcessingJob.started_at))
        .limit(1)
    )
    result = await db.execute(query)
    job = result.scalar_one_or_none()

    if not job or payload.force_restart:
        job = ProcessingJob(
            video_id=video_id,
            status="pending",
            current_stage="VALIDATE",
            progress_pct=0.0
        )
        db.add(job)
    else:
        if job.status == "failed" or job.status == "cancelled":
            job.status = "pending"
            job.error_message = None

    await db.commit()
    await db.refresh(job)

    logger.info(f"Processing job {job.id} queued for video {video_id}.")
    return ProcessingStatusResponse(
        job_id=job.id,
        video_id=job.video_id,
        status=job.status,
        current_stage=job.current_stage,
        progress_pct=job.progress_pct,
        error_message=job.error_message,
        retry_count=job.retry_count,
        stage_timings=job.stage_timings_json or {},
        started_at=job.started_at,
        completed_at=job.completed_at
    )
