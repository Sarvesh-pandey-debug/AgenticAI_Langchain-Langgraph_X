from abc import ABC, abstractmethod
from typing import Dict, Any, List

class EHRLoader(ABC):
    """
    Abstract Base Class for EHR Integrations.
    All adapters (Epic, eCW, Mock) must implement these methods.
    """
    
    @abstractmethod
    async def get_patient_encounter(self, patient_id: str, encounter_id: str) -> Dict[str, Any]:
        """
        Fetches full encounter data from the EHR.
        """
        pass

    @abstractmethod
    async def get_clinical_notes(self, encounter_id: str) -> str:
        """
        Extracts the text-based clinical notes/narrative from the encounter.
        """
        pass

    @abstractmethod
    async def search_patients(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for patients in the EHR system.
        """
        pass
