import asyncio
import sys
import os

# Ensure the app module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.models.mcr import ICD10Code, CPTCode

SAMPLE_ICD10 = [
    {"code": "J18.9", "description": "Pneumonia, unspecified organism", "category": "Respiratory"},
    {"code": "I10", "description": "Essential (primary) hypertension", "category": "Circulatory"},
    {"code": "E11.9", "description": "Type 2 diabetes mellitus without complications", "category": "Endocrine"},
    {"code": "R07.9", "description": "Chest pain, unspecified", "category": "Symptoms"},
    {"code": "R06.02", "description": "Shortness of breath", "category": "Symptoms"},
    {"code": "R11.2", "description": "Nausea with vomiting, unspecified", "category": "Symptoms"},
]

SAMPLE_CPT = [
    {"code": "99213", "description": "Office or other outpatient visit for the evaluation and management of an established patient, which requires a medically appropriate history and/or examination and low level of medical decision making.", "category": "E/M", "base_rvu": "1.39"},
    {"code": "99214", "description": "Office or other outpatient visit for the evaluation and management of an established patient, which requires a medically appropriate history and/or examination and moderate level of medical decision making.", "category": "E/M", "base_rvu": "1.92"},
    {"code": "93000", "description": "Electrocardiogram, routine ECG with at least 12 leads; with interpretation and report", "category": "Medicine", "base_rvu": "0.48"},
    {"code": "71045", "description": "Radiologic examination, chest; single view", "category": "Radiology", "base_rvu": "0.55"},
]

async def seed_data():
    print("🌱 Seeding Master Code Repository (MCR) data...")
    
    async with AsyncSessionLocal() as session:
        # Seed ICD-10
        print(f"Injecting {len(SAMPLE_ICD10)} ICD-10 codes...")
        for data in SAMPLE_ICD10:
            # Check if exists
            from sqlalchemy.future import select
            stmt = select(ICD10Code).where(ICD10Code.code == data["code"])
            result = await session.execute(stmt)
            if not result.scalars().first():
                code = ICD10Code(**data)
                session.add(code)
        
        # Seed CPT
        print(f"Injecting {len(SAMPLE_CPT)} CPT codes...")
        for data in SAMPLE_CPT:
            stmt = select(CPTCode).where(CPTCode.code == data["code"])
            result = await session.execute(stmt)
            if not result.scalars().first():
                code = CPTCode(**data)
                session.add(code)
                
        await session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed_data())
