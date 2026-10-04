import httpx
from typing import Dict, Any, List
from app.integrations.ehr.base import EHRLoader
from app.core.config import settings

class EpicFHIRClient(EHRLoader):
    """
    Epic FHIR R4 Adapter.
    Communicates with Epic's Interconnect FHIR APIs.
    """

    def __init__(self):
        self.base_url = settings.EPIC_BASE_URL
        self.client_id = settings.EPIC_CLIENT_ID
        self.headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json"
        }

    async def _get_auth_token(self) -> str:
        """
        Retrieves OAuth2 token from Epic. 
        In production, this would use private key JWT (RS256).
        For now, this is a placeholder for the OAuth flow.
        """
        # Placeholder for Epic's OAuth2 flow
        return "mock_epic_token"

    async def get_patient_encounter(self, patient_id: str, encounter_id: str) -> Dict[str, Any]:
        """
        Fetches a FHIR Encounter resource.
        Endpoint: [base]/Encounter/[id]
        """
        async with httpx.AsyncClient() as client:
            token = await self._get_auth_token()
            headers = {**self.headers, "Authorization": f"Bearer {token}"}
            
            response = await client.get(
                f"{self.base_url}/Encounter/{encounter_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()

    async def get_clinical_notes(self, encounter_id: str) -> str:
        """
        Fetches clinical notes associated with an encounter.
        In FHIR, these are often stored as 'DocumentReference' or 'ClinicalImpression'.
        """
        async with httpx.AsyncClient() as client:
            token = await self._get_auth_token()
            headers = {**self.headers, "Authorization": f"Bearer {token}"}
            
            # Epic often uses DocumentReference to store notes
            params = {"encounter": encounter_id, "category": "clinical-note"}
            response = await client.get(
                f"{self.base_url}/DocumentReference",
                headers=headers,
                params=params
            )
            
            if response.status_code != 200:
                return "Error fetching notes from Epic FHIR."
            
            data = response.json()
            # Logic to extract text from DocumentReference base64 or attachment
            # For now, we return a combined string of descriptions
            notes = []
            for entry in data.get("entry", []):
                doc = entry.get("resource", {})
                notes.append(doc.get("description", "No description provided."))
            
            return "\n".join(notes) if notes else "No clinical notes found for this encounter in Epic."

    async def search_patients(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for patients by name.
        Endpoint: [base]/Patient?name=[query]
        """
        async with httpx.AsyncClient() as client:
            token = await self._get_auth_token()
            headers = {**self.headers, "Authorization": f"Bearer {token}"}
            
            response = await client.get(
                f"{self.base_url}/Patient",
                headers=headers,
                params={"name": query}
            )
            response.raise_for_status()
            data = response.json()
            
            patients = []
            for entry in data.get("entry", []):
                p = entry.get("resource", {})
                patients.append({
                    "id": p.get("id"),
                    "name": p.get("name", [{}])[0].get("text", "Unknown"),
                    "dob": p.get("birthDate")
                })
            return patients
