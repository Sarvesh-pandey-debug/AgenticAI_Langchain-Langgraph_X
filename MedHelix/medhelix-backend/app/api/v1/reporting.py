from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def reporting_root():
    return {"message": "reporting router"}
