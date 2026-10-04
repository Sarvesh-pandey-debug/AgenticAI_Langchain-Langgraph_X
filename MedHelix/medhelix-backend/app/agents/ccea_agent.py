from app.agents.state import CodingState
from app.knowledge.clu.entity_extractor import CLUService

async def ccea_node(state: CodingState) -> dict:
    """
    Clinical Coding Extraction Agent (CCEA) Node.
    This is the first agent in the LangGraph pipeline.
    It takes the clinical note and extracts diagnoses, procedures, and symptoms.
    """
    note = state.get("clinical_note", "")
    
    # Initialize the CLU Service (simulating AWS Comprehend Medical)
    clu = CLUService()
    
    # Extract entities using Claude
    extracted_data = await clu.extract_entities(note)
    
    # Convert Pydantic models back to dictionaries for state
    entities = [entity.model_dump() for entity in extracted_data.entities]
    
    # Update the state
    return {
        "extracted_entities": entities,
        "audit_trail": ["CCEA successfully extracted clinical entities."]
    }
