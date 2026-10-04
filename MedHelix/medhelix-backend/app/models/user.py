from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import TimeStampedModel

class User(TimeStampedModel):
    """
    User model representing individuals logging into MedHelix.
    Users are associated with a specific tenant (unless they are super_admin).
    """
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True) # Optional if using Auth0
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # RBAC Role: 'super_admin', 'tenant_admin', 'coder', 'biller', 'viewer'
    role = Column(String(50), nullable=False, default="viewer")
    
    # Nullable because 'super_admin' might not belong to a single tenant
    tenant_id = Column(UUID(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Relationship
    tenant = relationship("Tenant")

    def __repr__(self):
        return f"<User(email={self.email}, role={self.role})>"
