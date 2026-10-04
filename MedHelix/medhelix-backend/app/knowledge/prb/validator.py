from typing import List, Dict, Any

class PRBValidator:
    """
    Payer Rules Brain (PRB) Validation Engine.
    Checks for NCCI bundling edits and payer-specific rules.
    """

    def __init__(self):
        # Mock bundling edits: (Code A, Code B) -> Requires Modifier
        self.bundling_edits = {
            ("99214", "93000"): True, # Office visit + EKG often needs Modifier 25
            ("99213", "93000"): True,
        }

    async def validate_codes(self, cpt_codes: List[str], icd_codes: List[str], modifiers: List[str]) -> Dict[str, Any]:
        """
        Validates the combination of codes.
        """
        issues = []
        flags = []
        
        # Check for bundling (NCCI)
        for i in range(len(cpt_codes)):
            for j in range(i + 1, len(cpt_codes)):
                pair = (cpt_codes[i], cpt_codes[j])
                rev_pair = (cpt_codes[j], cpt_codes[i])
                
                if pair in self.bundling_edits or rev_pair in self.bundling_edits:
                    if "25" not in modifiers and "59" not in modifiers:
                        issues.append(f"Potential bundling issue: {cpt_codes[i]} and {cpt_codes[j]} billed together without modifier.")
                        flags.append("NCCI_EDIT_WARNING")

        # Check for ICD-10 count
        if len(icd_codes) == 0:
            issues.append("No diagnosis codes (ICD-10) provided for the procedures.")
            flags.append("MISSING_DIAGNOSIS")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "flags": flags,
            "confidence_impact": -0.1 * len(issues) # Each issue reduces confidence
        }
