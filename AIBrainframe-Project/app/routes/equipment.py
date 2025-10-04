from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from config.database import get_db
from app.models import Equipment, EquipmentType, User
from app.schemas import EquipmentCreate, EquipmentResponse, EquipmentTypeCreate, EquipmentTypeResponse
from app.auth import get_current_user
from typing import List, Optional

router = APIRouter(prefix="/equipment", tags=["equipment"])

# Equipment endpoints
@router.post("/", response_model=EquipmentResponse)
def create_equipment(
    equipment_data: EquipmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new equipment"""

    # Create new equipment
    equipment = Equipment(
        equipment_name=equipment_data.equipment_name,
        manufacturer=equipment_data.manufacturer,
        model_number=equipment_data.model_number,
        equipment_type_id=equipment_data.equipment_type_id,
        serial_number=equipment_data.serial_number,
        installation_date=equipment_data.installation_date,
        location_description=equipment_data.location_description,
        job_id=equipment_data.job_id,
        company_id=current_user.company_id,
        status="active",
        notes=equipment_data.notes
    )

    db.add(equipment)
    db.commit()
    db.refresh(equipment)

    return equipment

@router.get("/", response_model=List[EquipmentResponse])
def get_equipment(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = Query(None, description="Filter by equipment status"),
    job_id: Optional[int] = Query(None, description="Filter by job ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get equipment list"""

    query = db.query(Equipment)

    # Filter by user's company if they have one
    if current_user.company_id:
        query = query.filter(Equipment.company_id == current_user.company_id)

    # Apply filters
    if status_filter:
        query = query.filter(Equipment.status == status_filter)
    if job_id:
        query = query.filter(Equipment.job_id == job_id)

    # Order by created date (newest first) and apply pagination
    equipment = query.order_by(Equipment.created_at.desc()).offset(skip).limit(limit).all()

    return equipment

@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment_by_id(
    equipment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific equipment by ID"""

    equipment = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()

    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )

    # Check if user has access to this equipment
    if current_user.company_id and equipment.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this equipment"
        )

    return equipment

@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    equipment_data: EquipmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update equipment details"""

    equipment = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()

    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )

    # Check if user has access to this equipment
    if current_user.company_id and equipment.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this equipment"
        )

    # Update equipment fields
    equipment.equipment_name = equipment_data.equipment_name
    equipment.manufacturer = equipment_data.manufacturer
    equipment.model_number = equipment_data.model_number
    equipment.equipment_type_id = equipment_data.equipment_type_id
    equipment.serial_number = equipment_data.serial_number
    equipment.installation_date = equipment_data.installation_date
    equipment.location_description = equipment_data.location_description
    equipment.job_id = equipment_data.job_id
    equipment.notes = equipment_data.notes

    db.commit()
    db.refresh(equipment)

    return equipment

@router.patch("/{equipment_id}/status")
def update_equipment_status(
    equipment_id: int,
    new_status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update equipment status"""

    valid_statuses = ["active", "maintenance", "out_of_service", "retired"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    equipment = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()

    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )

    # Check if user has access to this equipment
    if current_user.company_id and equipment.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this equipment"
        )

    equipment.status = new_status
    db.commit()

    return {"message": f"Equipment status updated to {new_status}", "equipment_id": equipment_id, "status": new_status}

@router.delete("/{equipment_id}")
def delete_equipment(
    equipment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete equipment (admin only)"""

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can delete equipment"
        )

    equipment = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()

    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )

    # Check if user has access to this equipment
    if current_user.company_id and equipment.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this equipment"
        )

    db.delete(equipment)
    db.commit()

    return {"message": "Equipment deleted successfully", "equipment_id": equipment_id}

# Equipment Types endpoints
@router.post("/types/", response_model=EquipmentTypeResponse)
def create_equipment_type(
    equipment_type_data: EquipmentTypeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new equipment type (admin only)"""

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can create equipment types"
        )

    equipment_type = EquipmentType(
        type_name=equipment_type_data.type_name,
        category=equipment_type_data.category,
        description=equipment_type_data.description,
        typical_maintenance_interval=equipment_type_data.typical_maintenance_interval,
        common_issues=equipment_type_data.common_issues,
        troubleshooting_guide=equipment_type_data.troubleshooting_guide
    )

    db.add(equipment_type)
    db.commit()
    db.refresh(equipment_type)

    return equipment_type

@router.get("/types/", response_model=List[EquipmentTypeResponse])
def get_equipment_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category_filter: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """Get equipment types list"""

    query = db.query(EquipmentType)

    if category_filter:
        query = query.filter(EquipmentType.category == category_filter)

    equipment_types = query.order_by(EquipmentType.type_name).offset(skip).limit(limit).all()

    return equipment_types

@router.get("/types/{equipment_type_id}", response_model=EquipmentTypeResponse)
def get_equipment_type(
    equipment_type_id: int,
    db: Session = Depends(get_db)
):
    """Get specific equipment type by ID"""

    equipment_type = db.query(EquipmentType).filter(
        EquipmentType.equipment_type_id == equipment_type_id
    ).first()

    if not equipment_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment type not found"
        )

    return equipment_type