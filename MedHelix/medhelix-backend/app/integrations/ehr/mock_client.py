from typing import Dict, Any, List
from app.integrations.ehr.base import EHRLoader

class MockEHRClient(EHRLoader):
    """
    Mock EHR Adapter for development and testing.
    Returns static data to simulate EHR responses without an API key.
    """

    async def get_patient_encounter(self, patient_id: str, encounter_id: str) -> Dict[str, Any]:
        return {
            "patient_id": patient_id,
            "encounter_id": encounter_id,
            "patient_name": "John Doe",
            "date": "2024-05-01",
            "facility": "MedHelix General Hospital",
            "practitioner": "Dr. Smith"
        }

    async def get_clinical_notes(self, encounter_id: str) -> str:
        # Simulate a real clinical note
        return (
            "CHIEF COMPLAINT: Severe chest pain and shortness of breath for 2 hours.\n"
            "HISTORY OF PRESENT ILLNESS: 55-year-old male with history of hypertension. "
            "Presents with crushing substernal chest pain. Denies nausea or vomiting.\n"
            "PHYSICAL EXAM: Tachycardic, BP 160/95. Lung sounds clear.\n"
            "PLAN: Order 12-lead EKG and chest X-ray. Rule out acute MI."
        )

    async def search_patients(self, query: str) -> List[Dict[str, Any]]:
        return [
            {"id": "pt-123", "name": "John Doe", "dob": "1970-01-01"},
            {"id": "pt-456", "name": "Jane Smith", "dob": "1985-06-15"}
        ]
