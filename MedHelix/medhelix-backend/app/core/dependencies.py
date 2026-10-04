from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token, UserRole
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

#Bearer Token Extractor 
bearer_scheme = HTTPBearer(auto_error=False)


#Current User Dependency 
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    FastAPI dependency: extracts and validates the JWT token.
    Returns the current user payload.

    Usage in routes:
        async def my_route(user = Depends(get_current_user)):
            print(user["user_id"])
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise credentials_exception

    return payload


#Tenant-Aware User 
async def get_current_tenant_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Ensures the current user has a tenant_id.
    Super admins can pass tenant_id in headers instead.
    """
    if not current_user.get("tenant_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tenant associated with this user",
        )
    return current_user


#RBAC Permission Dependencies 
def require_role(required_role: str):
    """
    Factory function that returns a dependency requiring a minimum role.

    Usage:
        @router.post("/submit", dependencies=[Depends(require_role("biller"))])
        async def submit_claim(...):
            ...
    """
    async def role_checker(
        current_user: dict = Depends(get_current_user)
    ) -> dict:
        user_role = current_user.get("role", "viewer")
        if not UserRole.has_permission(user_role, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires '{required_role}' role or higher. "
                       f"Your role: '{user_role}'",
            )
        return current_user
    return role_checker


#Prebuilt Role Guards 
require_super_admin = require_role(UserRole.SUPER_ADMIN)
require_tenant_admin = require_role(UserRole.TENANT_ADMIN)
require_coder = require_role(UserRole.CODER)
require_biller = require_role(UserRole.BILLER)
require_viewer = require_role(UserRole.VIEWER)


#Pagination Dependency 
class PaginationParams:
    """
    Reusable pagination parameters.

    Usage:
        async def list_claims(pagination: PaginationParams = Depends()):
            skip = pagination.skip
            limit = pagination.limit
    """
    def __init__(
        self,
        page: int = 1,
        page_size: int = settings.DEFAULT_PAGE_SIZE,
    ):
        if page < 1:
            page = 1
        if page_size > settings.MAX_PAGE_SIZE:
            page_size = settings.MAX_PAGE_SIZE
        self.page = page
        self.page_size = page_size
        self.skip = (page - 1) * page_size
        self.limit = page_size
