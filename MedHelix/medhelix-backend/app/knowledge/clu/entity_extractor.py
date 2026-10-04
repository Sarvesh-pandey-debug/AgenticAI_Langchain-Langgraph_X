from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_anthropic import ChatAnthropic
from app.core.config import settings

class MedicalEntity(BaseModel):
    text: str = Field(description="The exact text from the note")
    category: str = Field(description="One of: DIAGNOSIS, PROCEDURE, MEDICATION, SYMPTOM")
    is_negated: bool = Field(description="True if the provider stated the patient does NOT have this (e.g., 'denies nausea')")
    temporal_context: Optional[str] = Field(description="Any time context given (e.g., '3 days ago', 'chronic')", default=None)

class ExtractedClinicalData(BaseModel):
    entities: List[MedicalEntity]

class CLUService:
    """
    Clinical Language Understanding (CLU) Service.
    Currently acts as a Mock/Stub for AWS Comprehend Medical by using Anthropic's Claude 3 Haiku 
    to extract structured medical entities from clinical notes.
    """
    
    def __init__(self):
        # We use Haiku for fast, cheap entity extraction
        self.llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=0,
            api_key=settings.ANTHROPIC_API_KEY
        )
        self.structured_llm = self.llm.with_structured_output(ExtractedClinicalData)

    async def extract_entities(self, clinical_note: str) -> ExtractedClinicalData:
        """
        Extracts medical entities from a clinical note.
        """
        prompt = f"""
        You are an expert clinical natural language processing engine (similar to AWS Comprehend Medical).
        Read the following clinical note and extract all diagnoses, procedures, medications, and symptoms.
        Pay very close attention to NEGATION. If a patient 'denies' something or has 'no' symptom, mark is_negated=True.
        
        Clinical Note:
        {clinical_note}
        """
        
        result = await self.structured_llm.ainvoke(prompt)
        return result
