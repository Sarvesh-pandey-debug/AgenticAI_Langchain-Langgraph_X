from sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from app.models.base import TenantScopedModel
from datetime import datetime, timezone

class PatientIntake(TenantScopedModel):
    """Tracks the initial patient intake and eligibility process"""
    __tablename__ = "patient_intakes"

    patient_id = Column(String(100), index=True, nullable=False)
    encounter_id = Column(String(100), index=True, nullable=False)
    
    # EHR Data Snapshot
    patient_name = Column(String(255), nullable=True)
    date_of_service = Column(String(20), nullable=True)
    
    # Eligibility Status
    eligibility_status = Column(String(50), default="PENDING") # PENDING, ACTIVE, INACTIVE, ERROR
    eligibility_raw_response = Column(JSON, nullable=True)
    
    # Metadata
    status = Column(String(50), default="INTAKE_COMPLETED")
    
    def __repr__(self):
        return f"<PatientIntake(patient={self.patient_name}, status={self.eligibility_status})>"
