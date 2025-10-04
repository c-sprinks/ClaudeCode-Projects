from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from config.database import get_db
from app.models import Job, User
from app.schemas import JobCreate, JobResponse
from app.auth import get_current_user
from typing import List, Optional
from datetime import date

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job"""

    # Check if job number already exists
    existing_job = db.query(Job).filter(Job.job_number == job_data.job_number).first()
    if existing_job:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job number already exists"
        )

    # Create new job
    job = Job(
        job_number=job_data.job_number,
        title=job_data.title,
        description=job_data.description,
        customer_name=job_data.customer_name,
        customer_address=job_data.customer_address,
        customer_phone=job_data.customer_phone,
        assigned_user_id=current_user.user_id,
        company_id=current_user.company_id,
        priority=job_data.priority,
        job_type=job_data.job_type,
        status="assigned"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job

@router.get("/", response_model=List[JobResponse])
def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = Query(None, description="Filter by job status"),
    priority_filter: Optional[str] = Query(None, description="Filter by priority"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get jobs for current user"""

    query = db.query(Job)

    # Filter by user's company if they have one
    if current_user.company_id:
        query = query.filter(Job.company_id == current_user.company_id)
    else:
        # If no company, show only jobs assigned to the user
        query = query.filter(Job.assigned_user_id == current_user.user_id)

    # Apply filters
    if status_filter:
        query = query.filter(Job.status == status_filter)
    if priority_filter:
        query = query.filter(Job.priority == priority_filter)

    # Order by created date (newest first) and apply pagination
    jobs = query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()

    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific job by ID"""

    job = db.query(Job).filter(Job.job_id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # Check if user has access to this job
    if current_user.company_id:
        if job.company_id != current_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this job"
            )
    else:
        if job.assigned_user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this job"
            )

    return job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update job details"""

    job = db.query(Job).filter(Job.job_id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # Check if user has access to this job
    if current_user.company_id:
        if job.company_id != current_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this job"
            )
    else:
        if job.assigned_user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this job"
            )

    # Update job fields
    job.title = job_data.title
    job.description = job_data.description
    job.customer_name = job_data.customer_name
    job.customer_address = job_data.customer_address
    job.customer_phone = job_data.customer_phone
    job.priority = job_data.priority
    job.job_type = job_data.job_type

    db.commit()
    db.refresh(job)

    return job

@router.patch("/{job_id}/status")
def update_job_status(
    job_id: int,
    new_status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update job status"""

    valid_statuses = ["assigned", "in_progress", "completed", "cancelled", "on_hold"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    job = db.query(Job).filter(Job.job_id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # Check if user has access to this job
    if current_user.company_id:
        if job.company_id != current_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this job"
            )
    else:
        if job.assigned_user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this job"
            )

    # Update status and completion date if completing
    job.status = new_status
    if new_status == "completed":
        job.completed_date = date.today()

    db.commit()

    return {"message": f"Job status updated to {new_status}", "job_id": job_id, "status": new_status}

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a job (admin only)"""

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can delete jobs"
        )

    job = db.query(Job).filter(Job.job_id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # Check if user has access to this job
    if current_user.company_id and job.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this job"
        )

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully", "job_id": job_id}