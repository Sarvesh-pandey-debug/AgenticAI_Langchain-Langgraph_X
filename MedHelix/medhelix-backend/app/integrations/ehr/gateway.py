from app.core.config import settings
from app.integrations.ehr.base import EHRLoader
from app.integrations.ehr.mock_client import MockEHRClient
from app.integrations.ehr.epic_client import EpicFHIRClient
from app.integrations.ehr.ecw_client import ECWClient

class EHRGateway:
    """
    Gateway for EHR operations.
    Determines which EHR adapter to use based on the environment and client configuration.
    """
    
    @staticmethod
    def get_client(provider: str = "mock") -> EHRLoader:
        """
        Returns an instance of an EHR client.
        Supports: 'mock', 'epic', 'ecw'.
        """
        if provider == "epic" and settings.EPIC_CLIENT_ID:
            return EpicFHIRClient()
        
        if provider == "ecw" and settings.ECW_API_KEY:
            return ECWClient()
        
        # Default to Mock for development or if keys are missing
        return MockEHRClient()
