from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.redis import CacheService
from app.models.mcr import ICD10Code, CPTCode

class MCRLookupService:
    """
    Master Code Repository (MCR) Lookup Service.
    Provides fast, Redis-cached lookups for ICD-10 and CPT codes.
    """

    def __init__(self, db: AsyncSession, cache: CacheService):
        self.db = db
        self.cache = cache

    async def get_icd10(self, code: str) -> Optional[Dict[str, Any]]:
        """Look up an ICD-10 code (cached)"""
        code = code.upper().strip()
        cache_key = self.cache.icd10_key(code)
        
        # 1. Try Cache
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return cached_result
            
        # 2. Try Database
        stmt = select(ICD10Code).where(ICD10Code.code == code)
        result = await self.db.execute(stmt)
        db_record = result.scalars().first()
        
        if not db_record:
            return None
            
        # 3. Cache and Return
        result_dict = {
            "code": db_record.code,
            "description": db_record.description,
            "category": db_record.category,
            "is_billable": db_record.is_billable,
            "is_active": db_record.is_active
        }
        
        # Cache for 24 hours
        await self.cache.set(cache_key, result_dict, ttl=86400)
        
        return result_dict

    async def get_cpt(self, code: str) -> Optional[Dict[str, Any]]:
        """Look up a CPT procedure code (cached)"""
        code = code.upper().strip()
        cache_key = self.cache.cpt_key(code)
        
        # 1. Try Cache
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return cached_result
            
        # 2. Try Database
        stmt = select(CPTCode).where(CPTCode.code == code)
        result = await self.db.execute(stmt)
        db_record = result.scalars().first()
        
        if not db_record:
            return None
            
        # 3. Cache and Return
        result_dict = {
            "code": db_record.code,
            "description": db_record.description,
            "category": db_record.category,
            "base_rvu": db_record.base_rvu,
            "is_active": db_record.is_active
        }
        
        # Cache for 24 hours
        await self.cache.set(cache_key, result_dict, ttl=86400)
        
        return result_dict
