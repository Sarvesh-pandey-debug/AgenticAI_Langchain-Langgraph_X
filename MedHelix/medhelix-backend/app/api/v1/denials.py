from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def denials_root():
    return {"message": "denials router"}
