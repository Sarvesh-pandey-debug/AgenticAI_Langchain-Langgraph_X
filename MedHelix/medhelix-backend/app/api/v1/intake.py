from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.services.intake_service import IntakeService

router = APIRouter()

class IntakeRequest(BaseModel):
    patient_id: str
    encounter_id: str
    provider: str = "mock"
    tenant_id: str = "77777777-7777-7777-7777-777777777777" # Default for P0

@router.post("/process")
async def process_patient_intake(request: IntakeRequest, db: AsyncSession = Depends(get_db)):
    """
    Triggers the intake process for a patient.
    Fetches EHR data and verifies insurance eligibility.
    """
    try:
        service = IntakeService(db)
        result = await service.process_intake(
            patient_id=request.patient_id,
            encounter_id=request.encounter_id,
            provider=request.provider,
            tenant_id=request.tenant_id
        )
        return {
            "status": "success",
            "intake_id": result.id,
            "patient_name": result.patient_name,
            "eligibility": result.eligibility_status,
            "date_of_service": result.date_of_service
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
