from sqlalchemy import Column, String, Text, JSON, ForeignKey, DateTime
from app.models.base import TenantScopedModel
from datetime import datetime, timezone

class Appeal(TenantScopedModel):
    """Stores AI-generated insurance appeal letters"""
    __tablename__ = "appeals"

    claim_id = Column(String(100), index=True, nullable=False)
    encounter_id = Column(String(100), index=True, nullable=False)
    
    # Denial Info
    denial_reason_codes = Column(JSON, nullable=False)
    original_codes = Column(JSON, nullable=False)
    
    # Generated Content
    appeal_letter_text = Column(Text, nullable=False)
    
    # Status
    status = Column(String(50), default="DRAFT") # DRAFT, SENT, WON, LOST
    
    # Metadata
    generated_at = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Appeal(claim={self.claim_id}, status={self.status})>"
