import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class TimeStampedModel(Base):
    """Abstract base model with created_at and updated_at"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class TenantScopedModel(TimeStampedModel):
    """Abstract base model that enforces tenant isolation"""
    __abstract__ = True
    
    tenant_id = Column(UUID(as_uuid=False), index=True, nullable=False)
