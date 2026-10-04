from sqlalchemy import Column, String, Text, Float, JSON, ForeignKey, Boolean
from app.models.base import TenantScopedModel

class CodingHistory(TenantScopedModel):
    """Stores the complete history of an AI coding session"""
    __tablename__ = "coding_history"

    encounter_id = Column(String(100), index=True, nullable=False)
    patient_id = Column(String(100), index=True, nullable=False)
    
    # Input
    clinical_note = Column(Text, nullable=False)
    
    # AI Output
    ai_suggested_codes = Column(JSON, nullable=False) # List of ICD and CPT codes
    ai_confidence_score = Column(Float, nullable=False)
    ai_audit_trail = Column(JSON, nullable=True)
    
    # HITL Result (to be updated later by a human)
    human_approved_codes = Column(JSON, nullable=True)
    is_human_edited = Column(Boolean, default=False)
    feedback_notes = Column(Text, nullable=True)
    
    status = Column(String(50), default="PENDING") # PENDING, AUTO_APPROVED, HUMAN_REVIEWED

    def __repr__(self):
        return f"<CodingHistory(encounter={self.encounter_id}, status={self.status})>"
