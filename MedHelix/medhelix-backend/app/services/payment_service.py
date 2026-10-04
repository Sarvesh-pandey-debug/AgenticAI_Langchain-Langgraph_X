from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.claims import Claim
from app.models.payments import Payment
from app.integrations.clearinghouse.stedi_client import StediClient
from typing import Dict, Any

class PaymentService:
    """
    Service to handle ERA (Electronic Remittance Advice) processing.
    Updates claim status and posts payments/denials.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_remittance(self, claim_internal_id: str, tenant_id: str) -> Payment:
        """
        1. Fetch ERA from Stedi.
        2. Update the internal Claim status.
        3. Create a Payment record.
        """
        # Fetch the claim from DB
        result = await self.db.execute(select(Claim).where(Claim.id == claim_internal_id))
        claim = result.scalar_one_or_none()
        
        if not claim:
            raise ValueError(f"Claim {claim_internal_id} not found.")

        # Step 1: Fetch Remittance from Stedi
        stedi = StediClient()
        era_data = await stedi.fetch_remittance(claim.clearinghouse_claim_id)
        
        # Step 2: Update Claim Status
        new_status = era_data.get("status", "PAID")
        claim.status = new_status
        
        # Step 3: Create Payment Record
        payment = Payment(
            tenant_id=tenant_id,
            claim_id=claim.id,
            encounter_id=claim.encounter_id,
            amount_paid=era_data.get("amount_paid", 0.0),
            patient_responsibility=era_data.get("patient_responsibility", 0.0),
            adjustment_codes=era_data.get("adjustment_codes", []),
            status=new_status,
            raw_era_data=era_data
        )
        
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        
        return payment
