from sqlalchemy import Column, String, JSON, Float, ForeignKey, DateTime
from app.models.base import TenantScopedModel
from datetime import datetime, timezone

class Payment(TenantScopedModel):
    """Tracks ERA (Electronic Remittance Advice) and payment posting"""
    __tablename__ = "payments"

    claim_id = Column(String(100), index=True, nullable=False)
    encounter_id = Column(String(100), index=True, nullable=False)
    
    # Financial Details
    amount_paid = Column(Float, default=0.0)
    patient_responsibility = Column(Float, default=0.0)
    adjustment_amount = Column(Float, default=0.0)
    
    # Status & Codes
    status = Column(String(50), default="PROCESSED") # PROCESSED, DENIED, PARTIAL
    adjustment_codes = Column(JSON, nullable=True) # List of CARCs and RARCs
    
    # Metadata
    remittance_date = Column(DateTime, default=datetime.now(timezone.utc))
    raw_era_data = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Payment(claim={self.claim_id}, amount={self.amount_paid})>"
