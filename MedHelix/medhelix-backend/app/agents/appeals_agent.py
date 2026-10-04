import anthropic
from app.core.config import settings

class AppealsAgent:
    """
    AI Agent responsible for generating insurance appeal letters.
    Uses Claude 3.5 Sonnet for professional medical writing.
    """

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_appeal_letter(self, claim_data: dict, denial_reasons: list) -> str:
        """
        Generates a professional appeal letter based on claim data and denial reasons.
        """
        prompt = f"""
        You are a senior medical billing and appeals specialist at MedHelix.
        Write a professional and persuasive appeal letter to an insurance payer.
        
        CLAIM DETAILS:
        - Patient ID: {claim_data.get('patient_id')}
        - Encounter ID: {claim_data.get('encounter_id')}
        - Original ICD-10 Codes: {claim_data.get('icd10_codes')}
        - Original CPT Codes: {claim_data.get('cpt_codes')}
        
        DENIAL REASONS (CARC/RARC Codes):
        {denial_reasons}
        
        INSTRUCTIONS:
        1. Use a formal tone.
        2. Reference specific medical necessity.
        3. Addressing the denial reasons provided.
        4. Request re-evaluation of the claim.
        5. The letter should be complete and ready to send.
        """

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2000,
                temperature=0.7,
                system="You are an expert in medical billing and insurance appeals.",
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            # Fallback mock letter if API fails
            return f"MOCK APPEAL LETTER\n\nSubject: Appeal for Claim {claim_data.get('encounter_id')}\n\nWe are appealing the denial based on reasons: {denial_reasons}. The submitted codes are medically necessary for the patient's condition."
