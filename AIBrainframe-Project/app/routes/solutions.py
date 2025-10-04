from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from config.database import get_db
from app.models import Solution, User, EquipmentType
from app.schemas import SolutionCreate, SolutionResponse, SolutionRating
from app.auth import get_current_user
from typing import List, Optional
from decimal import Decimal

router = APIRouter(prefix="/solutions", tags=["solutions"])

@router.post("/", response_model=SolutionResponse)
def create_solution(
    solution_data: SolutionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new solution"""

    # Validate equipment type exists if provided
    if solution_data.equipment_type_id:
        equipment_type = db.query(EquipmentType).filter(
            EquipmentType.equipment_type_id == solution_data.equipment_type_id
        ).first()
        if not equipment_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipment type not found"
            )

    # Create new solution
    solution = Solution(
        title=solution_data.title,
        problem_description=solution_data.problem_description,
        solution_steps=solution_data.solution_steps,
        equipment_type_id=solution_data.equipment_type_id,
        difficulty_level=solution_data.difficulty_level,
        estimated_time=solution_data.estimated_time,
        created_by=current_user.user_id,
        company_id=current_user.company_id,
        is_verified=solution_data.is_verified if current_user.role in ["admin", "manager"] else False,
        usage_count=0,
        success_rate=None,
        average_rating=None
    )

    db.add(solution)
    db.commit()
    db.refresh(solution)

    return solution

@router.get("/", response_model=List[SolutionResponse])
def get_solutions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    equipment_type_id: Optional[int] = Query(None, description="Filter by equipment type"),
    difficulty_level: Optional[str] = Query(None, description="Filter by difficulty level"),
    verified_only: bool = Query(False, description="Show only verified solutions"),
    search: Optional[str] = Query(None, description="Search in title and problem description"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get solutions list with filtering and search"""

    query = db.query(Solution)

    # Filter by user's company if they have one, or show public solutions
    if current_user.company_id:
        query = query.filter(
            and_(
                Solution.company_id == current_user.company_id,
                Solution.is_verified == True
            )
        )
    else:
        # Show only verified public solutions for users without a company
        query = query.filter(Solution.is_verified == True)

    # Apply filters
    if equipment_type_id:
        query = query.filter(Solution.equipment_type_id == equipment_type_id)

    if difficulty_level:
        query = query.filter(Solution.difficulty_level == difficulty_level)

    if verified_only:
        query = query.filter(Solution.is_verified == True)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            func.lower(Solution.title).contains(search_term.lower()) |
            func.lower(Solution.problem_description).contains(search_term.lower())
        )

    # Order by average rating (desc), then usage count (desc), then created date (desc)
    solutions = query.order_by(
        Solution.average_rating.desc().nullslast(),
        Solution.usage_count.desc(),
        Solution.created_at.desc()
    ).offset(skip).limit(limit).all()

    return solutions

@router.get("/{solution_id}", response_model=SolutionResponse)
def get_solution(
    solution_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific solution by ID and increment usage count"""

    solution = db.query(Solution).filter(Solution.solution_id == solution_id).first()

    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )

    # Check if user has access to this solution
    if not solution.is_verified:
        if current_user.company_id != solution.company_id and current_user.user_id != solution.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this solution"
            )

    # Increment usage count
    solution.usage_count += 1
    db.commit()
    db.refresh(solution)

    return solution

@router.put("/{solution_id}", response_model=SolutionResponse)
def update_solution(
    solution_id: int,
    solution_data: SolutionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update solution (only by creator or admin)"""

    solution = db.query(Solution).filter(Solution.solution_id == solution_id).first()

    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )

    # Check if user can edit this solution
    if (solution.created_by != current_user.user_id and
        current_user.role not in ["admin", "manager"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only solution creator or admin can edit this solution"
        )

    # Update solution fields
    solution.title = solution_data.title
    solution.problem_description = solution_data.problem_description
    solution.solution_steps = solution_data.solution_steps
    solution.equipment_type_id = solution_data.equipment_type_id
    solution.difficulty_level = solution_data.difficulty_level
    solution.estimated_time = solution_data.estimated_time

    # Only admin/manager can change verification status
    if current_user.role in ["admin", "manager"]:
        solution.is_verified = solution_data.is_verified

    db.commit()
    db.refresh(solution)

    return solution

@router.patch("/{solution_id}/verify")
def verify_solution(
    solution_id: int,
    verified: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify/unverify a solution (admin only)"""

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can verify solutions"
        )

    solution = db.query(Solution).filter(Solution.solution_id == solution_id).first()

    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )

    solution.is_verified = verified
    db.commit()

    return {
        "message": f"Solution {'verified' if verified else 'unverified'} successfully",
        "solution_id": solution_id,
        "is_verified": verified
    }

@router.post("/{solution_id}/rate")
def rate_solution(
    solution_id: int,
    rating_data: SolutionRating,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rate a solution (1-5 stars)"""

    if not (1 <= rating_data.rating <= 5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )

    solution = db.query(Solution).filter(Solution.solution_id == solution_id).first()

    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )

    # For now, we'll store ratings in a simple way by calculating running average
    # In a production system, you'd want a separate ratings table
    if solution.average_rating is None:
        solution.average_rating = Decimal(str(rating_data.rating))
        rating_count = 1
    else:
        # Simple running average calculation (in production, store individual ratings)
        current_total = solution.average_rating * solution.usage_count
        new_total = current_total + Decimal(str(rating_data.rating))
        rating_count = solution.usage_count + 1
        solution.average_rating = new_total / rating_count

    db.commit()

    return {
        "message": "Solution rated successfully",
        "solution_id": solution_id,
        "new_average_rating": float(solution.average_rating),
        "your_rating": rating_data.rating
    }

@router.get("/search/similar")
def search_similar_solutions(
    problem_keywords: str = Query(..., description="Keywords describing the problem"),
    equipment_type_id: Optional[int] = Query(None, description="Equipment type filter"),
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search for similar solutions based on problem keywords"""

    query = db.query(Solution).filter(Solution.is_verified == True)

    # Filter by equipment type if provided
    if equipment_type_id:
        query = query.filter(Solution.equipment_type_id == equipment_type_id)

    # Search in title and problem description
    search_terms = problem_keywords.split()
    for term in search_terms:
        search_pattern = f"%{term}%"
        query = query.filter(
            func.lower(Solution.title).contains(search_pattern.lower()) |
            func.lower(Solution.problem_description).contains(search_pattern.lower())
        )

    # Order by relevance (average rating, usage count)
    solutions = query.order_by(
        Solution.average_rating.desc().nullslast(),
        Solution.usage_count.desc()
    ).limit(limit).all()

    return {
        "search_keywords": problem_keywords,
        "solutions_found": len(solutions),
        "solutions": [
            {
                "solution_id": sol.solution_id,
                "title": sol.title,
                "problem_description": sol.problem_description[:200] + "..." if len(sol.problem_description) > 200 else sol.problem_description,
                "difficulty_level": sol.difficulty_level,
                "average_rating": float(sol.average_rating) if sol.average_rating else None,
                "usage_count": sol.usage_count
            }
            for sol in solutions
        ]
    }

@router.delete("/{solution_id}")
def delete_solution(
    solution_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a solution (creator or admin only)"""

    solution = db.query(Solution).filter(Solution.solution_id == solution_id).first()

    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found"
        )

    # Check if user can delete this solution
    if (solution.created_by != current_user.user_id and
        current_user.role not in ["admin", "manager"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only solution creator or admin can delete this solution"
        )

    db.delete(solution)
    db.commit()

    return {"message": "Solution deleted successfully", "solution_id": solution_id}