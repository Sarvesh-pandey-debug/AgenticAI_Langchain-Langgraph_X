import operator
from typing import TypedDict, Annotated, List, Dict, Any

class CodingState(TypedDict):
    """
    The state dictionary that gets passed through the LangGraph agents.
    """
    
    # Input
    clinical_note: str
    patient_id: str
    encounter_id: str
    specialty: str
    payer_id: str

    # CCEA Output (Clinical Coding Extraction Agent)
    extracted_entities: List[Dict[str, Any]]
    
    # ICA Output (Intelligent Coding Agent) - Future
    suggested_icd10: List[Dict[str, Any]]
    suggested_cpt: List[Dict[str, Any]]
    modifiers: List[str]

    # CQAA Output (Coding Quality & Audit Agent) - Future
    validation_result: str
    ncci_edits: List[str]
    payer_rule_flags: List[str]
    confidence_score: float

    # CRLA Output (Coding Review & Learning Agent) - Future
    final_codes: List[str]
    hitl_required: bool
    audit_trail: Annotated[List[str], operator.add]
