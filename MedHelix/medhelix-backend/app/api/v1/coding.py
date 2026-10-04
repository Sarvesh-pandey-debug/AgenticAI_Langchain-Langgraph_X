from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.graph import coding_graph
from app.integrations.ehr.gateway import EHRGateway

router = APIRouter()

class ExtractRequest(BaseModel):
    clinical_note: str
    patient_id: str = "unknown"
    encounter_id: str = "unknown"
    specialty: str = "general"
    payer_id: str = "unknown"

class FetchRequest(BaseModel):
    patient_id: str
    encounter_id: str
    provider: str = "mock"

@router.post("/fetch-and-extract")
async def fetch_and_extract(request: FetchRequest):
    """
    1. Fetches clinical notes from an EHR (via MIG).
    2. Processes the note through the LangGraph AI pipeline.
    """
    try:
        # Step 1: Fetch from EHR Gateway
        ehr = EHRGateway.get_client(provider=request.provider)
        clinical_note = await ehr.get_clinical_notes(request.encounter_id)
        
        # Step 2: Prepare initial state for AI
        initial_state = {
            "clinical_note": clinical_note,
            "patient_id": request.patient_id,
            "encounter_id": request.encounter_id,
            "specialty": "General Medicine",
            "payer_id": "MEDICARE_CA", # Mock payer for now
            "extracted_entities": [],
            "suggested_icd10": [],
            "suggested_cpt": [],
            "modifiers": [],
            "audit_trail": [f"Successfully fetched clinical note from EHR ({request.provider})"]
        }
        
        # Step 3: Run LangGraph AI Pipeline
        final_state = await coding_graph.ainvoke(initial_state)
        
        return {
            "status": "success",
            "source": request.provider,
            "clinical_note": clinical_note,
            "extracted_entities": final_state.get("extracted_entities", []),
            "suggested_icd10": final_state.get("suggested_icd10", []),
            "suggested_cpt": final_state.get("suggested_cpt", []),
            "modifiers": final_state.get("modifiers", []),
            "validation_result": final_state.get("validation_result"),
            "ncci_edits": final_state.get("ncci_edits", []),
            "confidence_score": final_state.get("confidence_score"),
            "hitl_required": final_state.get("hitl_required"),
            "audit_trail": final_state.get("audit_trail", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract")
async def extract_coding_entities(request: ExtractRequest):
    """
    Passes a clinical note through the LangGraph AI pipeline.
    Currently runs the CCEA (Clinical Coding Extraction Agent) node.
    """
    try:
        # Initial State
        initial_state = {
            "clinical_note": request.clinical_note,
            "patient_id": request.patient_id,
            "encounter_id": request.encounter_id,
            "specialty": request.specialty,
            "payer_id": request.payer_id,
            "extracted_entities": [],
            "audit_trail": []
        }
        
        # Run the graph
        final_state = await coding_graph.ainvoke(initial_state)
        
        return {
            "status": "success",
            "extracted_entities": final_state.get("extracted_entities", []),
            "suggested_icd10": final_state.get("suggested_icd10", []),
            "suggested_cpt": final_state.get("suggested_cpt", []),
            "modifiers": final_state.get("modifiers", []),
            "validation_result": final_state.get("validation_result"),
            "ncci_edits": final_state.get("ncci_edits", []),
            "payer_rule_flags": final_state.get("payer_rule_flags", []),
            "confidence_score": final_state.get("confidence_score"),
            "final_codes": final_state.get("final_codes", []),
            "hitl_required": final_state.get("hitl_required", False),
            "audit_trail": final_state.get("audit_trail", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
