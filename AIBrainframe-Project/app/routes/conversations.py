from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db
from app.models import User, Conversation, ConversationMessage, Equipment
from app.schemas import ConversationCreate, MessageCreate, MessageResponse, ConversationResponse
from app.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/", response_model=ConversationResponse)
def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new AI troubleshooting conversation"""

    title = conversation_data.title or "New Troubleshooting Session"

    conversation = Conversation(
        user_id=current_user.user_id,
        job_id=conversation_data.job_id,
        equipment_id=conversation_data.equipment_id,
        title=title,
        ai_model="llama3.1",
        context_data={},
        started_at=datetime.utcnow()
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

@router.get("/", response_model=List[ConversationResponse])
def get_user_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user"""

    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.user_id
    ).order_by(Conversation.started_at.desc()).all()

    return conversations

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""

    # Verify user owns this conversation
    conversation = db.query(Conversation).filter(
        Conversation.conversation_id == conversation_id,
        Conversation.user_id == current_user.user_id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = db.query(ConversationMessage).filter(
        ConversationMessage.conversation_id == conversation_id
    ).order_by(ConversationMessage.timestamp).all()

    return messages

@router.post("/{conversation_id}/messages", response_model=MessageResponse)
def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response"""

    # Verify user owns this conversation
    conversation = db.query(Conversation).filter(
        Conversation.conversation_id == conversation_id,
        Conversation.user_id == current_user.user_id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Add user message to database
    user_message = ConversationMessage(
        conversation_id=conversation_id,
        sender_type="user",
        message_text=message_data.message_text,
        is_solution=message_data.is_solution,
        timestamp=datetime.utcnow()
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Generate AI response (simplified for now)
    ai_response_text = f"I understand you're having an issue: '{message_data.message_text}'. Let me help you troubleshoot this step by step. Can you provide more details about the specific problem you're experiencing?"

    # Add AI response to database
    ai_message = ConversationMessage(
        conversation_id=conversation_id,
        sender_type="ai",
        message_text=ai_response_text,
        timestamp=datetime.utcnow()
    )

    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    return ai_message