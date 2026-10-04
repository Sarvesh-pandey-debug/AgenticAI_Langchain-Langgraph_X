from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.services.payment_service import PaymentService

router = APIRouter()

class RemittanceRequest(BaseModel):
    claim_id: str
    tenant_id: str = "77777777-7777-7777-7777-777777777777"

@router.post("/process-era")
async def process_remittance(request: RemittanceRequest, db: AsyncSession = Depends(get_db)):
    """
    Simulates fetching and processing an ERA for a specific claim.
    """
    try:
        service = PaymentService(db)
        payment = await service.process_remittance(
            claim_internal_id=request.claim_id,
            tenant_id=request.tenant_id
        )
        return {
            "status": "success",
            "payment_id": payment.id,
            "claim_status": payment.status,
            "amount_paid": payment.amount_paid,
            "adjustment_codes": payment.adjustment_codes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
