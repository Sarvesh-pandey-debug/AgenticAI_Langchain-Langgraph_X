from langchain.tools import tool
from typing import Optional, Dict, Any
from app.knowledge.mcr.lookup import MCRLookupService
from app.core.database import AsyncSessionLocal
from app.core.redis import get_redis, CacheService

@tool
async def lookup_icd10_code(code: str) -> str:
    """
    Search for a specific ICD-10 diagnosis code in the Master Code Repository.
    Returns the description and category if found.
    """
    async with AsyncSessionLocal() as db:
        redis = await get_redis()
        cache = CacheService(redis)
        service = MCRLookupService(db, cache)
        result = await service.get_icd10(code)
        if result:
            return f"Code: {result['code']}, Description: {result['description']}, Category: {result['category']}"
        return f"ICD-10 code {code} not found in repository."

@tool
async def lookup_cpt_code(code: str) -> str:
    """
    Search for a specific CPT procedure code in the Master Code Repository.
    Returns the description and RVU if found.
    """
    async with AsyncSessionLocal() as db:
        redis = await get_redis()
        cache = CacheService(redis)
        service = MCRLookupService(db, cache)
        result = await service.get_cpt(code)
        if result:
            return f"Code: {result['code']}, Description: {result['description']}, Category: {result['category']}, RVU: {result['base_rvu']}"
        return f"CPT code {code} not found in repository."
