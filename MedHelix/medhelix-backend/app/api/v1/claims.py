from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.services.claim_service import ClaimService

router = APIRouter()

class ClaimSubmitRequest(BaseModel):
    patient_id: str
    encounter_id: str
    icd10_codes: List[str]
    cpt_codes: List[str]
    modifiers: Optional[List[str]] = []
    tenant_id: str = "77777777-7777-7777-7777-777777777777"

@router.post("/submit")
async def submit_medical_claim(request: ClaimSubmitRequest, db: AsyncSession = Depends(get_db)):
    """
    Submits a new medical claim to the clearinghouse.
    """
    try:
        service = ClaimService(db)
        claim = await service.create_and_submit_claim(
            patient_id=request.patient_id,
            encounter_id=request.encounter_id,
            icd10_codes=request.icd10_codes,
            cpt_codes=request.cpt_codes,
            tenant_id=request.tenant_id,
            modifiers=request.modifiers
        )
        return {
            "status": "success",
            "claim_id": claim.id,
            "stedi_claim_id": claim.clearinghouse_claim_id,
            "submission_status": claim.status,
            "total_charge": claim.total_charge
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
