from app.agents.state import CodingState
from app.core.config import settings

async def crla_node(state: CodingState) -> dict:
    """
    Coding Review & Learning Agent (CRLA) Node.
    Finalizes the coding session and determines if human review is required.
    """
    confidence = state.get("confidence_score", 0.0)
    validation = state.get("validation_result", "FAIL")
    
    # Thresholds from settings (or defaults)
    hitl_threshold = settings.CODING_CONFIDENCE_THRESHOLD # e.g. 0.85
    
    # Decision Logic
    hitl_required = False
    if confidence < hitl_threshold:
        hitl_required = True
        reason = f"Confidence score ({confidence:.2f}) is below threshold ({hitl_threshold})."
    elif validation == "FAIL":
        hitl_required = True
        reason = "Validation failed (CQAA flags found)."
    else:
        reason = "AI confidence is high and validation passed. Auto-approval eligible."

    # Finalize codes
    suggested_icd = [s["code"] for s in state.get("suggested_icd10", [])]
    suggested_cpt = [s["code"] for s in state.get("suggested_cpt", [])]
    final_codes = suggested_icd + suggested_cpt

    return {
        "final_codes": final_codes,
        "hitl_required": hitl_required,
        "audit_trail": [f"CRLA finalized session. HITL Required: {hitl_required}. Reason: {reason}"]
    }
