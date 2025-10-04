from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from config.database import get_db
from app.models import Company, User
from app.schemas import CompanyCreate, CompanyResponse
from app.auth import get_current_user
from typing import List, Optional

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=CompanyResponse)
def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company (admin only)"""

    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create companies"
        )

    # Check if company name already exists
    existing_company = db.query(Company).filter(
        Company.company_name == company_data.company_name
    ).first()
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company name already exists"
        )

    # Create new company
    company = Company(
        company_name=company_data.company_name,
        address=company_data.address,
        phone=company_data.phone,
        email=company_data.email,
        subscription_level=company_data.subscription_level,
        is_active=True
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

@router.get("/", response_model=List[CompanyResponse])
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    subscription_level: Optional[str] = Query(None, description="Filter by subscription level"),
    active_only: bool = Query(True, description="Show only active companies"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get companies list (admin only)"""

    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all companies"
        )

    query = db.query(Company)

    # Apply filters
    if active_only:
        query = query.filter(Company.is_active == True)

    if subscription_level:
        query = query.filter(Company.subscription_level == subscription_level)

    # Order by company name and apply pagination
    companies = query.order_by(Company.company_name).offset(skip).limit(limit).all()

    return companies

@router.get("/my-company", response_model=CompanyResponse)
def get_my_company(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's company information"""

    if not current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not associated with any company"
        )

    company = db.query(Company).filter(
        Company.company_id == current_user.company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    return company

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific company by ID"""

    company = db.query(Company).filter(Company.company_id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    # Check permissions - admin can see all, users can only see their own company
    if current_user.role not in ["admin", "super_admin"]:
        if current_user.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this company"
            )

    return company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update company details"""

    company = db.query(Company).filter(Company.company_id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    # Check permissions - admin can edit all, managers can edit their own company
    if current_user.role not in ["admin", "super_admin"]:
        if current_user.company_id != company_id or current_user.role != "manager":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins or company managers can edit company details"
            )

    # Update company fields
    company.company_name = company_data.company_name
    company.address = company_data.address
    company.phone = company_data.phone
    company.email = company_data.email

    # Only admin can change subscription level
    if current_user.role in ["admin", "super_admin"]:
        company.subscription_level = company_data.subscription_level

    db.commit()
    db.refresh(company)

    return company

@router.patch("/{company_id}/status")
def update_company_status(
    company_id: int,
    is_active: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activate/deactivate a company (admin only)"""

    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change company status"
        )

    company = db.query(Company).filter(Company.company_id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    company.is_active = is_active
    db.commit()

    status_text = "activated" if is_active else "deactivated"
    return {
        "message": f"Company {status_text} successfully",
        "company_id": company_id,
        "is_active": is_active
    }

@router.patch("/{company_id}/subscription")
def update_subscription_level(
    company_id: int,
    subscription_level: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update company subscription level (admin only)"""

    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change subscription levels"
        )

    valid_levels = ["basic", "standard", "premium", "enterprise"]
    if subscription_level not in valid_levels:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid subscription level. Must be one of: {', '.join(valid_levels)}"
        )

    company = db.query(Company).filter(Company.company_id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    company.subscription_level = subscription_level
    db.commit()

    return {
        "message": "Subscription level updated successfully",
        "company_id": company_id,
        "subscription_level": subscription_level
    }

@router.get("/{company_id}/users", response_model=List[dict])
def get_company_users(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get users associated with a company"""

    # Check permissions
    if current_user.role not in ["admin", "super_admin"]:
        if current_user.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this company's users"
            )

    # Verify company exists
    company = db.query(Company).filter(Company.company_id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    # Get users for this company
    users = db.query(User).filter(
        User.company_id == company_id
    ).order_by(User.full_name).offset(skip).limit(limit).all()

    # Return limited user information (no sensitive data)
    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
        for user in users
    ]

@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a company (super admin only)"""

    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete companies"
        )

    company = db.query(Company).filter(Company.company_id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    # Check if company has active users
    user_count = db.query(User).filter(
        User.company_id == company_id,
        User.is_active == True
    ).count()

    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete company with {user_count} active users. Deactivate users first."
        )

    db.delete(company)
    db.commit()

    return {"message": "Company deleted successfully", "company_id": company_id}