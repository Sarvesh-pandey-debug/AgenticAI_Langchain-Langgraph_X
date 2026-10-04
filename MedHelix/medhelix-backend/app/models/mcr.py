from sqlalchemy import Column, String, Boolean, Text
from app.models.base import TimeStampedModel

class ICD10Code(TimeStampedModel):
    """Master repository for ICD-10 Diagnosis Codes"""
    __tablename__ = "icd10_codes"

    code = Column(String(20), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    is_billable = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<ICD10Code(code={self.code})>"


class CPTCode(TimeStampedModel):
    """Master repository for CPT Procedure Codes"""
    __tablename__ = "cpt_codes"

    code = Column(String(20), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True) # e.g., 'E/M', 'Surgery'
    base_rvu = Column(String(20), nullable=True) # Relative Value Unit
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<CPTCode(code={self.code})>"
