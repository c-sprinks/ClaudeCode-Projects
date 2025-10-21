from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: str = "technician"
    company_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Conversation schemas
class ConversationCreate(BaseModel):
    title: Optional[str] = None
    equipment_id: Optional[int] = None
    job_id: Optional[int] = None

class MessageCreate(BaseModel):
    message_text: str
    is_solution: Optional[bool] = False

class MessageResponse(BaseModel):
    message_id: int
    conversation_id: int
    sender_type: str
    message_text: str
    timestamp: datetime
    is_solution: bool

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    conversation_id: int
    title: str
    status: str
    started_at: datetime

    class Config:
        from_attributes = True

# Job schemas
class JobCreate(BaseModel):
    job_number: str
    title: str
    description: Optional[str] = None
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    customer_phone: Optional[str] = None
    priority: str = "medium"
    job_type: Optional[str] = None

class JobResponse(BaseModel):
    job_id: int
    job_number: str
    title: str
    status: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True

# Equipment schemas
class EquipmentCreate(BaseModel):
    equipment_name: str
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    equipment_type_id: Optional[int] = None
    serial_number: Optional[str] = None
    installation_date: Optional[date] = None
    location_description: Optional[str] = None
    job_id: Optional[int] = None
    notes: Optional[str] = None

class EquipmentResponse(BaseModel):
    equipment_id: int
    equipment_name: str
    manufacturer: Optional[str]
    model_number: Optional[str]
    serial_number: Optional[str]
    location_description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Equipment Type schemas
class EquipmentTypeCreate(BaseModel):
    type_name: str
    category: str
    description: Optional[str] = None
    typical_maintenance_interval: Optional[int] = None
    common_issues: Optional[str] = None
    troubleshooting_guide: Optional[str] = None

class EquipmentTypeResponse(BaseModel):
    equipment_type_id: int
    type_name: str
    category: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Solution schemas
class SolutionCreate(BaseModel):
    title: str
    problem_description: str
    solution_steps: str
    equipment_type_id: Optional[int] = None
    difficulty_level: str = "medium"
    estimated_time: Optional[int] = None
    is_verified: Optional[bool] = False

class SolutionResponse(BaseModel):
    solution_id: int
    title: str
    problem_description: str
    solution_steps: str
    difficulty_level: str
    estimated_time: Optional[int]
    success_rate: Optional[Decimal]
    is_verified: bool
    usage_count: int
    average_rating: Optional[Decimal]
    created_at: datetime

    class Config:
        from_attributes = True

class SolutionRating(BaseModel):
    rating: int  # 1-5 stars
    feedback: Optional[str] = None

# Company schemas
class CompanyCreate(BaseModel):
    company_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    subscription_level: str = "basic"

class CompanyResponse(BaseModel):
    company_id: int
    company_name: str
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    subscription_level: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str