from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.services.appeals_service import AppealsService

router = APIRouter()

class AppealGenerateRequest(BaseModel):
    claim_id: str
    tenant_id: str = "77777777-7777-7777-7777-777777777777"

@router.post("/generate")
async def generate_claim_appeal(request: AppealGenerateRequest, db: AsyncSession = Depends(get_db)):
    """
    Triggers the AI Appeals Agent to write an appeal letter for a denied claim.
    """
    try:
        service = AppealsService(db)
        appeal = await service.generate_automated_appeal(
            claim_id=request.claim_id,
            tenant_id=request.tenant_id
        )
        return {
            "status": "success",
            "appeal_id": appeal.id,
            "status": appeal.status,
            "letter_preview": appeal.appeal_letter_text[:500] + "..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
