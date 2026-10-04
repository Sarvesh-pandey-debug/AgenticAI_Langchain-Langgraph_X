from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def hitl_root():
    return {"message": "hitl router"}
