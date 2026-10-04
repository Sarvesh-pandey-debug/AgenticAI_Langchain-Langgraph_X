from app.agents.state import CodingState
from app.knowledge.prb.validator import PRBValidator

async def cqaa_node(state: CodingState) -> dict:
    """
    Coding Quality & Audit Agent (CQAA) Node.
    Validates the suggested codes against payer rules and NCCI edits.
    """
    icd_suggestions = state.get("suggested_icd10", [])
    cpt_suggestions = state.get("suggested_cpt", [])
    modifiers = state.get("modifiers", [])
    
    # Extract just the code strings for the validator
    icd_codes = [s["code"] for s in icd_suggestions]
    cpt_codes = [s["code"] for s in cpt_suggestions]
    
    # Run Validation
    validator = PRBValidator()
    validation_results = await validator.validate_codes(cpt_codes, icd_codes, modifiers)
    
    # Calculate final confidence score (start from average of ICA scores)
    avg_confidence = 0.0
    if (len(icd_suggestions) + len(cpt_suggestions)) > 0:
        total_conf = sum(s.get("confidence", 0.0) for s in icd_suggestions) + \
                     sum(s.get("confidence", 0.0) for s in cpt_suggestions)
        avg_confidence = total_conf / (len(icd_suggestions) + len(cpt_suggestions))
    
    final_confidence = max(0.0, min(1.0, avg_confidence + validation_results["confidence_impact"]))

    return {
        "validation_result": "PASS" if validation_results["is_valid"] else "FAIL",
        "ncci_edits": validation_results["issues"],
        "payer_rule_flags": validation_results["flags"],
        "confidence_score": final_confidence,
        "audit_trail": ["CQAA audited the codes and found " + ("no issues." if validation_results["is_valid"] else f"{len(validation_results['issues'])} issues.")]
    }
