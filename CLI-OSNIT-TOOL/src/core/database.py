"""
Inspector-G Database Management

SQLAlchemy-based database setup for storing investigation results,
user preferences, and OSINT intelligence data.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
from pathlib import Path

from src.core.config import settings

Base = declarative_base()

class Investigation(Base):
    """Investigation session model"""
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    investigation_type = Column(String(50), nullable=False)  # username, email, phone, domain, ai
    target = Column(String(255), nullable=False)
    status = Column(String(20), default="pending")  # pending, in_progress, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    metadata = Column(JSON, default={})

    # Relationships
    results = relationship("InvestigationResult", back_populates="investigation")

class InvestigationResult(Base):
    """Individual results from investigations"""
    __tablename__ = "investigation_results"

    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    source = Column(String(100), nullable=False)  # Platform/source of the result
    result_type = Column(String(50), nullable=False)  # found, not_found, error, etc.
    data = Column(JSON)  # The actual result data
    confidence = Column(Integer, default=50)  # Confidence score 0-100
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    investigation = relationship("Investigation", back_populates="results")

class UserPreference(Base):
    """User preferences and settings"""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    value_type = Column(String(20), default="string")  # string, int, bool, json
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class OSINTSource(Base):
    """OSINT sources and their configurations"""
    __tablename__ = "osint_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    source_type = Column(String(50), nullable=False)  # username, email, phone, domain
    base_url = Column(String(255))
    enabled = Column(Boolean, default=True)
    rate_limit = Column(Integer, default=1)  # Requests per second
    requires_auth = Column(Boolean, default=False)
    auth_config = Column(JSON, default={})
    custom_headers = Column(JSON, default={})

class CacheEntry(Base):
    """Cache for investigation results"""
    __tablename__ = "cache_entries"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String(255), unique=True, nullable=False)
    cache_value = Column(Text)
    cache_type = Column(String(50), default="investigation")
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DatabaseManager:
    """Database manager for Inspector-G"""

    def __init__(self):
        self.database_url = self._get_database_url()
        self.engine = create_engine(
            self.database_url,
            echo=settings.database_echo,
            connect_args={"check_same_thread": False} if "sqlite" in self.database_url else {}
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _get_database_url(self) -> str:
        """Get database URL with proper path resolution"""
        if settings.database_url.startswith("sqlite:///~/"):
            # Expand home directory for SQLite
            db_path = Path(settings.database_url.replace("sqlite:///~/", "")).expanduser()
            db_path.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite:///{db_path}"
        return settings.database_url

    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_investigation(self, investigation_type: str, target: str, metadata: Optional[Dict] = None) -> Investigation:
        """Create a new investigation"""
        db = next(self.get_session())
        try:
            investigation = Investigation(
                investigation_type=investigation_type,
                target=target,
                metadata=metadata or {}
            )
            db.add(investigation)
            db.commit()
            db.refresh(investigation)
            return investigation
        finally:
            db.close()

    def add_result(self, investigation_id: int, source: str, result_type: str,
                  data: Dict, confidence: int = 50) -> InvestigationResult:
        """Add a result to an investigation"""
        db = next(self.get_session())
        try:
            result = InvestigationResult(
                investigation_id=investigation_id,
                source=source,
                result_type=result_type,
                data=data,
                confidence=confidence
            )
            db.add(result)
            db.commit()
            db.refresh(result)
            return result
        finally:
            db.close()

    def update_investigation_status(self, investigation_id: int, status: str) -> None:
        """Update investigation status"""
        db = next(self.get_session())
        try:
            investigation = db.query(Investigation).filter(Investigation.id == investigation_id).first()
            if investigation:
                investigation.status = status
                if status == "completed":
                    investigation.completed_at = datetime.utcnow()
                db.commit()
        finally:
            db.close()

    def get_investigation_history(self, limit: int = 50) -> List[Investigation]:
        """Get recent investigation history"""
        db = next(self.get_session())
        try:
            return db.query(Investigation).order_by(Investigation.created_at.desc()).limit(limit).all()
        finally:
            db.close()

    def get_investigation_results(self, investigation_id: int) -> List[InvestigationResult]:
        """Get all results for an investigation"""
        db = next(self.get_session())
        try:
            return db.query(InvestigationResult).filter(
                InvestigationResult.investigation_id == investigation_id
            ).order_by(InvestigationResult.created_at).all()
        finally:
            db.close()

    def set_preference(self, key: str, value: Any, value_type: str = "string") -> None:
        """Set a user preference"""
        db = next(self.get_session())
        try:
            # Convert value to string based on type
            if value_type == "json":
                str_value = json.dumps(value)
            elif value_type == "bool":
                str_value = str(bool(value))
            elif value_type == "int":
                str_value = str(int(value))
            else:
                str_value = str(value)

            # Update or create preference
            pref = db.query(UserPreference).filter(UserPreference.key == key).first()
            if pref:
                pref.value = str_value
                pref.value_type = value_type
                pref.updated_at = datetime.utcnow()
            else:
                pref = UserPreference(key=key, value=str_value, value_type=value_type)
                db.add(pref)

            db.commit()
        finally:
            db.close()

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        db = next(self.get_session())
        try:
            pref = db.query(UserPreference).filter(UserPreference.key == key).first()
            if not pref:
                return default

            # Convert string value back to proper type
            if pref.value_type == "json":
                return json.loads(pref.value)
            elif pref.value_type == "bool":
                return pref.value.lower() in ("true", "1", "yes")
            elif pref.value_type == "int":
                return int(pref.value)
            else:
                return pref.value
        finally:
            db.close()

    def cache_set(self, key: str, value: Any, cache_type: str = "investigation",
                 expires_at: Optional[datetime] = None) -> None:
        """Set a cache entry"""
        db = next(self.get_session())
        try:
            # Remove existing entry
            db.query(CacheEntry).filter(CacheEntry.cache_key == key).delete()

            # Add new entry
            cache_entry = CacheEntry(
                cache_key=key,
                cache_value=json.dumps(value) if isinstance(value, (dict, list)) else str(value),
                cache_type=cache_type,
                expires_at=expires_at
            )
            db.add(cache_entry)
            db.commit()
        finally:
            db.close()

    def cache_get(self, key: str) -> Optional[Any]:
        """Get a cache entry"""
        db = next(self.get_session())
        try:
            entry = db.query(CacheEntry).filter(CacheEntry.cache_key == key).first()
            if not entry:
                return None

            # Check if expired
            if entry.expires_at and entry.expires_at < datetime.utcnow():
                db.delete(entry)
                db.commit()
                return None

            # Try to parse as JSON, fall back to string
            try:
                return json.loads(entry.cache_value)
            except json.JSONDecodeError:
                return entry.cache_value
        finally:
            db.close()

# Global database manager instance
db_manager = DatabaseManager()