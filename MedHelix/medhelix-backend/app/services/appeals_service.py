from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.claims import Claim
from app.models.payments import Payment
from app.models.appeals import Appeal
from app.agents.appeals_agent import AppealsAgent

class AppealsService:
    """
    Service to orchestrate the automated appeals process.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_automated_appeal(self, claim_id: str, tenant_id: str) -> Appeal:
        """
        1. Identify the denied claim and its reasons.
        2. Call AI Appeals Agent to generate letter.
        3. Save the appeal draft.
        """
        # Fetch the denied claim
        result = await self.db.execute(select(Claim).where(Claim.id == claim_id))
        claim = result.scalar_one_or_none()
        
        if not claim:
            raise ValueError(f"Claim {claim_id} not found.")
            
        # Fetch the payment/denial record to get reasons
        p_result = await self.db.execute(
            select(Payment).where(Payment.claim_id == claim_id).order_by(Payment.remittance_date.desc())
        )
        payment = p_result.scalar_one_or_none()
        
        reasons = payment.adjustment_codes if payment else ["Unknown denial reason"]
        
        # Step 2: Generate Letter via AI
        agent = AppealsAgent()
        claim_data = {
            "patient_id": claim.patient_id,
            "encounter_id": claim.encounter_id,
            "icd10_codes": claim.icd10_codes,
            "cpt_codes": claim.cpt_codes
        }
        letter_text = await agent.generate_appeal_letter(claim_data, reasons)
        
        # Step 3: Save Appeal Record
        appeal = Appeal(
            tenant_id=tenant_id,
            claim_id=claim.id,
            encounter_id=claim.encounter_id,
            denial_reason_codes=reasons,
            original_codes=claim.icd10_codes + claim.cpt_codes,
            appeal_letter_text=letter_text,
            status="DRAFT"
        )
        
        self.db.add(appeal)
        await self.db.commit()
        await self.db.refresh(appeal)
        
        return appeal
