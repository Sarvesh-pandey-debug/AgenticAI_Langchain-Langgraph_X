from sqlalchemy import Column, String, JSON, Float, ForeignKey, DateTime
from app.models.base import TenantScopedModel
from datetime import datetime, timezone

class Claim(TenantScopedModel):
    """Stores medical insurance claims and their submission status"""
    __tablename__ = "claims"

    encounter_id = Column(String(100), index=True, nullable=False)
    patient_id = Column(String(100), index=True, nullable=False)
    
    # Coding Data
    icd10_codes = Column(JSON, nullable=False)
    cpt_codes = Column(JSON, nullable=False)
    modifiers = Column(JSON, nullable=True)
    
    # Financials
    total_charge = Column(Float, default=0.0)
    
    # Submission Status
    status = Column(String(50), default="READY") # READY, SUBMITTED, ACCEPTED, REJECTED, PAID, DENIED
    clearinghouse_claim_id = Column(String(100), nullable=True)
    submission_date = Column(DateTime, nullable=True)
    
    # Full Response
    raw_response = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Claim(encounter={self.encounter_id}, status={self.status})>"
