from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey, JSON, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    subscription_level = Column(String(20), default='basic')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    role = Column(String(20), default='technician')
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    job_number = Column(String(50), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    customer_name = Column(String(100))
    customer_address = Column(Text)
    customer_phone = Column(String(20))
    assigned_user_id = Column(Integer, ForeignKey('users.user_id'))
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    priority = Column(String(20), default='medium')
    status = Column(String(20), default='assigned')
    job_type = Column(String(50))
    scheduled_date = Column(Date)
    completed_date = Column(Date)
    estimated_hours = Column(DECIMAL(5,2))
    actual_hours = Column(DECIMAL(5,2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class EquipmentType(Base):
    __tablename__ = "equipment_types"

    equipment_type_id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    typical_maintenance_interval = Column(Integer)
    common_issues = Column(Text)
    troubleshooting_guide = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String(100), nullable=False)
    manufacturer = Column(String(100))
    model_number = Column(String(100))
    equipment_type_id = Column(Integer, ForeignKey('equipment_types.equipment_type_id'))
    serial_number = Column(String(100))
    installation_date = Column(Date)
    location_description = Column(Text)
    job_id = Column(Integer, ForeignKey('jobs.job_id'))
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    status = Column(String(20), default='active')
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.job_id'))
    equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'))
    title = Column(String(200))
    status = Column(String(20), default='active')
    ai_model = Column(String(50))
    context_data = Column(JSON)
    started_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    message_id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.conversation_id'), nullable=False)
    sender_type = Column(String(10), nullable=False)
    message_text = Column(Text, nullable=False)
    message_metadata = Column(JSON)
    is_solution = Column(Boolean, default=False)
    confidence_score = Column(DECIMAL(3,2))
    timestamp = Column(DateTime, default=datetime.utcnow)

class Solution(Base):
    __tablename__ = "solutions"

    solution_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    problem_description = Column(Text, nullable=False)
    solution_steps = Column(Text, nullable=False)
    equipment_type_id = Column(Integer, ForeignKey('equipment_types.equipment_type_id'))
    difficulty_level = Column(String(20), default='medium')
    estimated_time = Column(Integer)
    success_rate = Column(DECIMAL(5,2))
    created_by = Column(Integer, ForeignKey('users.user_id'))
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    is_verified = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)
    average_rating = Column(DECIMAL(3,2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    file_path = Column(String(500))
    file_type = Column(String(50))
    file_size = Column(Integer)
    equipment_type_id = Column(Integer, ForeignKey('equipment_types.equipment_type_id'))
    document_category = Column(String(50))
    is_public = Column(Boolean, default=False)
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    uploaded_by = Column(Integer, ForeignKey('users.user_id'))
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class JobActivity(Base):
    __tablename__ = "job_activities"

    activity_id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.job_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'))
    solution_id = Column(Integer, ForeignKey('solutions.solution_id'))
    time_spent = Column(DECIMAL(5,2))
    parts_used = Column(Text)
    notes = Column(Text)
    activity_date = Column(DateTime, default=datetime.utcnow)

class Attachment(Base):
    __tablename__ = "attachments"

    attachment_id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    attached_to_table = Column(String(50), nullable=False)
    attached_to_id = Column(Integer, nullable=False)
    uploaded_by = Column(Integer, ForeignKey('users.user_id'))
    upload_date = Column(DateTime, default=datetime.utcnow)

class SystemLog(Base):
    __tablename__ = "system_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    action = Column(String(100), nullable=False)
    table_name = Column(String(50))
    record_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)