from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.db.database import get_db
from backend.app.db.models import Video, TranscriptSegment, Note

router = APIRouter(prefix="/videos/{video_id}", tags=["Exports"])


def format_timestamp_srt(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    s = int(seconds)
    secs = s % 60
    mins = (s // 60) % 60
    hours = s // 3600
    return f"{hours:02d}:{mins:02d}:{secs:02d},{millis:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    s = int(seconds)
    secs = s % 60
    mins = (s // 60) % 60
    hours = s // 3600
    return f"{hours:02d}:{mins:02d}:{secs:02d}.{millis:03d}"


@router.get("/export/{export_format}")
async def export_video_data(
    video_id: str,
    export_format: str,
    db: AsyncSession = Depends(get_db)
):
    """Export video transcript or notes into markdown, txt, srt, vtt, or json."""
    v_res = await db.execute(select(Video).where(Video.id == video_id))
    video = v_res.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found.")

    seg_res = await db.execute(
        select(TranscriptSegment)
        .where(TranscriptSegment.video_id == video_id)
        .order_by(TranscriptSegment.segment_index)
    )
    segments = seg_res.scalars().all()

    fmt = export_format.lower()

    if fmt == "srt":
        lines = []
        for i, s in enumerate(segments, 1):
            lines.append(str(i))
            lines.append(f"{format_timestamp_srt(s.start_time)} --> {format_timestamp_srt(s.end_time)}")
            lines.append(s.text.strip())
            lines.append("")
        content = "\n".join(lines)
        return Response(content=content, media_type="text/plain", headers={"Content-Disposition": f"attachment; filename={video_id}.srt"})

    elif fmt == "vtt":
        lines = ["WEBVTT", ""]
        for i, s in enumerate(segments, 1):
            lines.append(str(i))
            lines.append(f"{format_timestamp_vtt(s.start_time)} --> {format_timestamp_vtt(s.end_time)}")
            lines.append(s.text.strip())
            lines.append("")
        content = "\n".join(lines)
        return Response(content=content, media_type="text/vtt", headers={"Content-Disposition": f"attachment; filename={video_id}.vtt"})

    elif fmt == "txt":
        content = "\n".join(f"[{format_timestamp_srt(s.start_time)}] {s.text}" for s in segments)
        return Response(content=content, media_type="text/plain", headers={"Content-Disposition": f"attachment; filename={video_id}.txt"})

    elif fmt == "markdown" or fmt == "md":
        header = f"# {video.title}\n\n*Source: {video.source_url or 'Local'}*\n\n## Transcript\n\n"
        body = "\n\n".join(f"**[{format_timestamp_srt(s.start_time)}]** {s.text}" for s in segments)
        return Response(content=header + body, media_type="text/markdown", headers={"Content-Disposition": f"attachment; filename={video_id}.md"})

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported export format: {export_format}. Supported: srt, vtt, txt, markdown")
