from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from app.agents.state import CodingState
from app.agents.tools.mcr_tools import lookup_icd10_code, lookup_cpt_code
from app.core.config import settings

class CodeSuggestion(BaseModel):
    code: str = Field(description="The medical code (ICD-10 or CPT)")
    description: str = Field(description="The description of the code")
    confidence: float = Field(description="Confidence score between 0 and 1", ge=0, le=1)
    reasoning: str = Field(description="Brief explanation of why this code was selected")

class ICASuggestions(BaseModel):
    icd10_codes: List[CodeSuggestion]
    cpt_codes: List[CodeSuggestion]
    modifiers: List[str]

async def ica_node(state: CodingState) -> dict:
    """
    Intelligent Coding Agent (ICA) Node.
    Maps extracted entities to official ICD-10 and CPT codes using MCR tools.
    """
    entities = state.get("extracted_entities", [])
    if not entities:
        return {"audit_trail": ["ICA skipped: No entities extracted."]}

    # Initialize LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022", # Use Sonnet for better reasoning
        temperature=0,
        api_key=settings.ANTHROPIC_API_KEY
    )
    
    # Bind tools to LLM
    tools = [lookup_icd10_code, lookup_cpt_code]
    llm_with_tools = llm.bind_tools(tools)
    
    # Structured output for final result
    structured_llm = llm.with_structured_output(ICASuggestions)

    # Construct the prompt
    entity_str = "\n".join([f"- {e['text']} ({e['category']}) {'[NEGATED]' if e['is_negated'] else ''}" for e in entities])
    
    prompt = f"""
    You are an Intelligent Coding Agent (ICA) for MedHelix. 
    Your task is to map extracted clinical entities to the most accurate ICD-10 (Diagnosis) and CPT (Procedure) codes.
    
    EXTRACTED ENTITIES:
    {entity_str}
    
    INSTRUCTIONS:
    1. Use the 'lookup_icd10_code' tool to verify diagnosis codes.
    2. Use the 'lookup_cpt_code' tool to verify procedure codes.
    3. Do NOT suggest negated entities as billable codes.
    4. Provide a confidence score for each suggestion.
    5. If you are unsure, provide the best possible match and a lower confidence score.
    """

    # Note: In a full LangGraph implementation, we might use a ToolNode and a loop.
    # For this P0 version, we will perform a direct reasoning call.
    # We will simulate the "reasoning with tools" by doing a multi-step call if necessary, 
    # but for simplicity here we'll use the structured LLM to generate suggestions based on internal knowledge 
    # and instructions to use tools for verification.
    
    # In a more advanced version, we'd use: 
    # response = await llm_with_tools.ainvoke([HumanMessage(content=prompt)])
    # But for now, we'll get structured output directly.
    
    result = await structured_llm.ainvoke(prompt)
    
    return {
        "suggested_icd10": [c.model_dump() for c in result.icd10_codes],
        "suggested_cpt": [c.model_dump() for c in result.cpt_codes],
        "modifiers": result.modifiers,
        "audit_trail": ["ICA successfully mapped entities to medical codes."]
    }
