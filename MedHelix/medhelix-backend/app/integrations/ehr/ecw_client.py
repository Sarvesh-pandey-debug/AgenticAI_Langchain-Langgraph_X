import httpx
from typing import Dict, Any, List
from app.integrations.ehr.base import EHRLoader
from app.core.config import settings

class ECWClient(EHRLoader):
    """
    eClinicalWorks (eCW) REST API Adapter.
    Communicates with eCW's developer portal APIs.
    """

    def __init__(self):
        self.base_url = settings.ECW_BASE_URL
        self.api_key = settings.ECW_API_KEY
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    async def get_patient_encounter(self, patient_id: str, encounter_id: str) -> Dict[str, Any]:
        """
        Fetches encounter details from eCW.
        Endpoint: [base]/encounter/{id}
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/encounter/{encounter_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_clinical_notes(self, encounter_id: str) -> str:
        """
        Fetches Progress Notes (HPI, ROS, Exam) from eCW.
        """
        async with httpx.AsyncClient() as client:
            # eCW often stores notes in a separate 'progress-notes' endpoint
            response = await client.get(
                f"{self.base_url}/encounter/{encounter_id}/progress-notes",
                headers=self.headers
            )
            
            if response.status_code != 200:
                return "Error fetching progress notes from eCW."
            
            data = response.json()
            # eCW notes are often segmented by section (HPI, Exam, etc.)
            sections = data.get("sections", [])
            full_note = []
            for sec in sections:
                name = sec.get("name", "Unknown Section")
                text = sec.get("text", "")
                full_note.append(f"--- {name} ---\n{text}")
            
            return "\n\n".join(full_note) if full_note else "No clinical notes found for this eCW encounter."

    async def search_patients(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for patients in eCW.
        Endpoint: [base]/patient/search
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/patient/search",
                headers=self.headers,
                json={"name": query}
            )
            response.raise_for_status()
            data = response.json()
            
            patients = []
            for p in data.get("patients", []):
                patients.append({
                    "id": p.get("patient_id"),
                    "name": f"{p.get('first_name')} {p.get('last_name')}",
                    "dob": p.get("dob")
                })
            return patients
