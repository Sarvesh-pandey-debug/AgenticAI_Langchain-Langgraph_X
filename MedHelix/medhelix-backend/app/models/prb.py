from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedModel

class Payer(TimeStampedModel):
    """List of insurance payers supported by MedHelix"""
    __tablename__ = "payers"

    name = Column(String(255), nullable=False)
    payer_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. 'MEDICARE_CA'
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Payer(name={self.name})>"


class PayerRule(TimeStampedModel):
    """Payer-specific billing and coding rules"""
    __tablename__ = "payer_rules"

    payer_id = Column(String(50), ForeignKey("payers.payer_id", ondelete="CASCADE"), nullable=False)
    rule_code = Column(String(100), index=True, nullable=False) # e.g. 'MODIFIER_REQUIRED'
    cpt_code = Column(String(20), index=True, nullable=True) # Optional: Rule applies to specific CPT
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)

    payer = relationship("Payer")

    def __repr__(self):
        return f"<PayerRule(code={self.rule_code})>"


class NCCIEdit(TimeStampedModel):
    """NCCI Procedure-to-Procedure (PTP) edits / Bundling rules"""
    __tablename__ = "ncci_edits"

    code_1 = Column(String(20), index=True, nullable=False) # Column 1 code
    code_2 = Column(String(20), index=True, nullable=False) # Column 2 code (bundled into code_1)
    modifier_allowed = Column(Boolean, default=False)      # Can a modifier bypass this?
    effective_date = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<NCCIEdit(pair={self.code_1}/{self.code_2})>"
