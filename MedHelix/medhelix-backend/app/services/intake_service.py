from sqlalchemy.ext.asyncio import AsyncSession
from app.models.intake import PatientIntake
from app.integrations.ehr.gateway import EHRGateway
from app.integrations.clearinghouse.stedi_client import StediClient
from typing import Dict, Any

class IntakeService:
    """
    Service to handle the patient intake process.
    Orchestrates EHR data fetching and Eligibility verification.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_intake(self, patient_id: str, encounter_id: str, provider: str, tenant_id: str) -> PatientIntake:
        """
        1. Fetch patient data from EHR.
        2. Verify eligibility via Clearinghouse.
        3. Save intake record.
        """
        # Step 1: EHR Fetch
        ehr = EHRGateway.get_client(provider=provider)
        encounter_data = await ehr.get_patient_encounter(patient_id, encounter_id)
        
        # Step 2: Eligibility Check
        stedi = StediClient()
        # Mock payer ID for the patient (in reality, would come from EHR data)
        payer_id = "MEDICARE_CA" 
        eligibility_result = await stedi.check_eligibility(encounter_data, payer_id)
        
        # Step 3: Create Database Record
        intake = PatientIntake(
            tenant_id=tenant_id,
            patient_id=patient_id,
            encounter_id=encounter_id,
            patient_name=encounter_data.get("patient_name"),
            date_of_service=encounter_data.get("date"),
            eligibility_status=eligibility_result.get("status", "UNKNOWN").upper(),
            eligibility_raw_response=eligibility_result
        )
        
        self.db.add(intake)
        await self.db.commit()
        await self.db.refresh(intake)
        
        return intake
