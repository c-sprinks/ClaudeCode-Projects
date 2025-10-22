from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from config.database import get_db
from app.models import Attachment, User, Job, Equipment, Conversation
from app.auth import get_current_user
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
import mimetypes

router = APIRouter(prefix="/attachments", tags=["attachments"])

# Configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
    'audio': ['.mp3', '.wav', '.ogg', '.m4a', '.aac'],
    'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz']
}

def get_file_category(filename: str) -> str:
    """Determine file category based on extension"""
    ext = Path(filename).suffix.lower()
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return category
    return 'other'

def validate_file(file: UploadFile) -> tuple[bool, str]:
    """Validate uploaded file"""
    # Check file size
    if hasattr(file, 'size') and file.size > MAX_FILE_SIZE:
        return False, f"File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit"

    # Check file extension
    ext = Path(file.filename).suffix.lower()
    all_allowed = []
    for extensions in ALLOWED_EXTENSIONS.values():
        all_allowed.extend(extensions)

    if ext not in all_allowed:
        return False, f"File type {ext} not allowed. Allowed types: {', '.join(all_allowed)}"

    return True, "Valid"

def check_table_access(user: User, table_name: str, record_id: int, db: Session) -> bool:
    """Check if user has access to attach files to specific record"""
    if table_name == "jobs":
        job = db.query(Job).filter(Job.job_id == record_id).first()
        return job and (
            job.assigned_user_id == user.user_id or
            job.company_id == user.company_id
        )
    elif table_name == "equipment":
        equipment = db.query(Equipment).filter(Equipment.equipment_id == record_id).first()
        return equipment and equipment.company_id == user.company_id
    elif table_name == "conversations":
        conversation = db.query(Conversation).filter(Conversation.conversation_id == record_id).first()
        return conversation and conversation.user_id == user.user_id

    return False

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    attached_to_table: str = Form(...),
    attached_to_id: int = Form(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload file and attach to specified record"""

    # Validate table name
    valid_tables = ["jobs", "equipment", "conversations"]
    if attached_to_table not in valid_tables:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid table name. Must be one of: {', '.join(valid_tables)}"
        )

    # Check access permissions
    if not check_table_access(current_user, attached_to_table, attached_to_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this record"
        )

    # Validate file
    is_valid, error_msg = validate_file(file)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    try:
        # Create secure filename
        file_ext = Path(file.filename).suffix.lower()
        secure_filename = f"{uuid.uuid4()}{file_ext}"

        # Create directory structure
        upload_path = UPLOAD_DIR / attached_to_table / str(attached_to_id)
        upload_path.mkdir(parents=True, exist_ok=True)

        # Full file path
        file_path = upload_path / secure_filename

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get file info
        file_size = file_path.stat().st_size
        mime_type, _ = mimetypes.guess_type(str(file_path))

        # Create database record
        attachment = Attachment(
            filename=secure_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            mime_type=mime_type or 'application/octet-stream',
            attached_to_table=attached_to_table,
            attached_to_id=attached_to_id,
            uploaded_by=current_user.user_id
        )

        db.add(attachment)
        db.commit()
        db.refresh(attachment)

        return {
            "attachment_id": attachment.attachment_id,
            "filename": attachment.original_filename,
            "file_size": attachment.file_size,
            "mime_type": attachment.mime_type,
            "category": get_file_category(attachment.original_filename),
            "upload_date": attachment.upload_date,
            "message": "File uploaded successfully"
        }

    except Exception as e:
        # Clean up file if database operation fails
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@router.get("/{table_name}/{record_id}")
def get_attachments(
    table_name: str,
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all attachments for a specific record"""

    # Validate table name
    valid_tables = ["jobs", "equipment", "conversations"]
    if table_name not in valid_tables:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid table name. Must be one of: {', '.join(valid_tables)}"
        )

    # Check access permissions
    if not check_table_access(current_user, table_name, record_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this record"
        )

    # Get attachments
    attachments = db.query(Attachment).filter(
        Attachment.attached_to_table == table_name,
        Attachment.attached_to_id == record_id
    ).order_by(Attachment.upload_date.desc()).all()

    return [
        {
            "attachment_id": att.attachment_id,
            "filename": att.original_filename,
            "file_size": att.file_size,
            "mime_type": att.mime_type,
            "category": get_file_category(att.original_filename),
            "upload_date": att.upload_date,
            "uploaded_by": att.uploaded_by
        } for att in attachments
    ]

@router.get("/download/{attachment_id}")
async def download_file(
    attachment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download specific file"""

    attachment = db.query(Attachment).filter(
        Attachment.attachment_id == attachment_id
    ).first()

    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )

    # Check access permissions
    if not check_table_access(current_user, attachment.attached_to_table, attachment.attached_to_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this attachment"
        )

    # Check if file exists
    file_path = Path(attachment.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )

    from fastapi.responses import FileResponse
    return FileResponse(
        path=str(file_path),
        filename=attachment.original_filename,
        media_type=attachment.mime_type
    )

@router.delete("/{attachment_id}")
def delete_attachment(
    attachment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete attachment"""

    attachment = db.query(Attachment).filter(
        Attachment.attachment_id == attachment_id
    ).first()

    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )

    # Check access permissions (only uploader or admin can delete)
    if (attachment.uploaded_by != current_user.user_id and
        current_user.role not in ["admin", "manager"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the uploader or admin can delete this attachment"
        )

    try:
        # Delete file from disk
        file_path = Path(attachment.file_path)
        if file_path.exists():
            file_path.unlink()

        # Delete database record
        db.delete(attachment)
        db.commit()

        return {"message": "Attachment deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete failed: {str(e)}"
        )

# Job-specific endpoints for convenience
@router.post("/jobs/{job_id}/upload")
async def upload_job_file(
    job_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload file to specific job"""
    return await upload_file(
        file=file,
        attached_to_table="jobs",
        attached_to_id=job_id,
        description=description,
        current_user=current_user,
        db=db
    )

@router.get("/jobs/{job_id}")
def get_job_attachments(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all attachments for specific job"""
    return get_attachments("jobs", job_id, current_user, db)

# Equipment-specific endpoints
@router.post("/equipment/{equipment_id}/upload")
async def upload_equipment_file(
    equipment_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload file to specific equipment"""
    return await upload_file(
        file=file,
        attached_to_table="equipment",
        attached_to_id=equipment_id,
        description=description,
        current_user=current_user,
        db=db
    )

@router.get("/equipment/{equipment_id}")
def get_equipment_attachments(
    equipment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all attachments for specific equipment"""
    return get_attachments("equipment", equipment_id, current_user, db)

# Conversation-specific endpoints
@router.post("/conversations/{conversation_id}/upload")
async def upload_conversation_file(
    conversation_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload file to specific conversation"""
    return await upload_file(
        file=file,
        attached_to_table="conversations",
        attached_to_id=conversation_id,
        description=description,
        current_user=current_user,
        db=db
    )

@router.get("/conversations/{conversation_id}")
def get_conversation_attachments(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all attachments for specific conversation"""
    return get_attachments("conversations", conversation_id, current_user, db)