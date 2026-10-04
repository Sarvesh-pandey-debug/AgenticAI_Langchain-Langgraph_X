from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def assistant_root():
    return {"message": "assistant router"}
