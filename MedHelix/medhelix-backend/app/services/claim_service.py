from sqlalchemy.ext.asyncio import AsyncSession
from app.models.claims import Claim
from app.integrations.clearinghouse.stedi_client import StediClient
from datetime import datetime, timezone
from typing import Dict, Any, List

class ClaimService:
    """
    Service to handle medical insurance claim submission.
    Links AI coding results to Clearinghouse EDI transactions.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_and_submit_claim(
        self, 
        patient_id: str, 
        encounter_id: str, 
        icd10_codes: List[str], 
        cpt_codes: List[str], 
        tenant_id: str,
        modifiers: List[str] = None
    ) -> Claim:
        """
        1. Formats the claim data.
        2. Submits to Stedi Clearinghouse.
        3. Saves the claim record in DB.
        """
        # Step 1: Prepare Claim Data (Simplified for Stedi 837P)
        claim_payload = {
            "submitter": {"name": "MedHelix Billing"},
            "receiver": {"name": "Medicare"},
            "patient": {"id": patient_id},
            "encounter": {"id": encounter_id},
            "diagnosis_codes": icd10_codes,
            "service_lines": [
                {"procedure_code": code, "units": 1, "charge": 150.0} for code in cpt_codes
            ]
        }
        
        # Step 2: Submit to Stedi
        stedi = StediClient()
        submission_result = await stedi.submit_claim(claim_payload)
        
        # Step 3: Create Database Record
        total_charge = sum(line["charge"] for line in claim_payload["service_lines"])
        
        claim = Claim(
            tenant_id=tenant_id,
            patient_id=patient_id,
            encounter_id=encounter_id,
            icd10_codes=icd10_codes,
            cpt_codes=cpt_codes,
            modifiers=modifiers,
            total_charge=total_charge,
            status="SUBMITTED",
            clearinghouse_claim_id=submission_result.get("claim_id"),
            submission_date=datetime.now(timezone.utc),
            raw_response=submission_result
        )
        
        self.db.add(claim)
        await self.db.commit()
        await self.db.refresh(claim)
        
        return claim
