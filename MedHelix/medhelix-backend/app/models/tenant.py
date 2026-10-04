from sqlalchemy import Column, String, Boolean
from app.models.base import TimeStampedModel

class Tenant(TimeStampedModel):
    """
    MedHelix Multi-Tenant Model.
    Each healthcare organization or billing company is a Tenant.
    """
    __tablename__ = "tenants"

    name = Column(String(255), nullable=False)
    domain = Column(String(255), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    branding_logo_url = Column(String(1024), nullable=True)
    branding_primary_color = Column(String(20), nullable=True)
    
    # Billing/usage tracking for SaaS
    subscription_plan = Column(String(50), default="standard")
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name={self.name})>"
