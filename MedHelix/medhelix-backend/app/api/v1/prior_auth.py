from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def prior_auth_root():
    return {"message": "prior_auth router"}
