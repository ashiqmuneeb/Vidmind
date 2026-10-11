from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.app.db.database import get_db
from backend.app.db.models import Video, Note
from backend.app.schemas.note import NoteResponse, NoteUpdateRequest, NoteGenerateRequest
from backend.app.core.logging import logger

router = APIRouter(prefix="/videos/{video_id}", tags=["Notes"])


@router.get("/notes", response_model=List[NoteResponse])
async def get_notes(
    video_id: str,
    style: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve notes generated for a video."""
    query = select(Note).where(Note.video_id == video_id)
    if style:
        query = query.where(Note.style == style)
    query = query.order_by(desc(Note.updated_at))

    result = await db.execute(query)
    notes = result.scalars().all()
    return [NoteResponse.model_validate(n) for n in notes]


@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
    video_id: str,
    note_id: str,
    payload: NoteUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Update editable user notes."""
    result = await db.execute(select(Note).where(Note.id == note_id, Note.video_id == video_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")

    note.markdown_content = payload.markdown_content
    if payload.title:
        note.title = payload.title
    note.is_user_edited = True

    await db.commit()
    await db.refresh(note)
    return NoteResponse.model_validate(note)
