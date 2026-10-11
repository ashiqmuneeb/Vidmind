from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.app.db.database import get_db
from backend.app.db.models import Video, ChatSession, ChatMessage
from backend.app.schemas.chat import ChatMessageRequest, ChatMessageResponse, CitationItem
from backend.app.core.logging import logger

router = APIRouter(prefix="/videos/{video_id}", tags=["Chat & Q&A"])


@router.get("/chat/messages", response_model=List[ChatMessageResponse])
async def list_chat_messages(
    video_id: str,
    session_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve chat message history for a video."""
    query = (
        select(ChatMessage)
        .join(ChatSession)
        .where(ChatSession.video_id == video_id)
        .order_by(ChatMessage.created_at)
    )
    if session_id:
        query = query.where(ChatMessage.session_id == session_id)

    result = await db.execute(query)
    messages = result.scalars().all()
    return [
        ChatMessageResponse(
            id=m.id,
            session_id=m.session_id,
            role=m.role,
            content=m.content,
            question_type=m.question_type,
            evidence_citations=m.evidence_citations_json or [],
            confidence_score=m.confidence_score,
            created_at=m.created_at
        )
        for m in messages
    ]


@router.post("/chat", response_model=ChatMessageResponse)
async def send_chat_message(
    video_id: str,
    payload: ChatMessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """Submit a user question about the video."""
    # Ensure video exists
    v_res = await db.execute(select(Video).where(Video.id == video_id))
    video = v_res.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found.")

    # Find or create session
    session_id = payload.session_id
    if not session_id:
        new_session = ChatSession(video_id=video_id, title=payload.message[:50])
        db.add(new_session)
        await db.flush()
        session_id = new_session.id

    # Record user message
    user_msg = ChatMessage(
        session_id=session_id,
        role="user",
        content=payload.message
    )
    db.add(user_msg)

    # In Phase 1 Foundation, return grounded placeholder acknowledging evidence retrieval
    assistant_msg = ChatMessage(
        session_id=session_id,
        role="assistant",
        content="I am ready to answer grounded questions about this video once transcription is indexed.",
        question_type="general",
        evidence_citations_json=[],
        confidence_score=1.0
    )
    db.add(assistant_msg)
    await db.commit()
    await db.refresh(assistant_msg)

    return ChatMessageResponse(
        id=assistant_msg.id,
        session_id=assistant_msg.session_id,
        role=assistant_msg.role,
        content=assistant_msg.content,
        question_type=assistant_msg.question_type,
        evidence_citations=[],
        confidence_score=1.0,
        created_at=assistant_msg.created_at
    )
