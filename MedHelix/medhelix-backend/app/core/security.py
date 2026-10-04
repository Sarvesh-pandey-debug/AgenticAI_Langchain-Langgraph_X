from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
import httpx
import logging

logger = logging.getLogger(__name__)

# Password Hashing 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against stored hash"""
    return pwd_context.verify(plain_password, hashed_password)


#JWT Tokens (Local Auth — used in Dev without Auth0)
def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    Used in development when Auth0 is not configured.
    In production, tokens are issued by Auth0.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(hours=24)
    )
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    })
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    Returns payload dict or None if invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode failed: {e}")
        return None


#Auth0 Token Verification (Production) 
class Auth0Verifier:
    """
    Verifies Auth0 JWT tokens in production.
    Fetches public keys from Auth0 JWKS endpoint.
    """

    def __init__(self):
        self.domain = settings.AUTH0_DOMAIN
        self.audience = settings.AUTH0_AUDIENCE
        self.algorithms = settings.AUTH0_ALGORITHMS
        self._jwks = None

    async def get_jwks(self) -> dict:
        """Fetch Auth0 public keys (cached)"""
        if not self._jwks:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"https://{self.domain}/.well-known/jwks.json"
                )
                self._jwks = resp.json()
        return self._jwks

    async def verify_token(self, token: str) -> Optional[dict]:
        """Verify Auth0 JWT and return payload"""
        try:
            jwks = await self.get_jwks()
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}

            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }

            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.algorithms,
                    audience=self.audience,
                    issuer=f"https://{self.domain}/",
                )
                return payload
        except JWTError as e:
            logger.warning(f"Auth0 token verification failed: {e}")
        return None


# ── RBAC Role Definitions 
class UserRole:
    SUPER_ADMIN = "super_admin"     # Platform-level admin (all tenants)
    TENANT_ADMIN = "tenant_admin"   # Tenant-level admin
    CODER = "coder"                 # Medical coder
    BILLER = "biller"               # Billing staff
    VIEWER = "viewer"               # Read-only access

    # Role hierarchy — higher index = more permissions
    HIERARCHY = [
        "viewer",
        "biller",
        "coder",
        "tenant_admin",
        "super_admin",
    ]

    @classmethod
    def has_permission(cls, user_role: str, required_role: str) -> bool:
        """Check if user_role has at least required_role permissions"""
        try:
            user_level = cls.HIERARCHY.index(user_role)
            required_level = cls.HIERARCHY.index(required_role)
            return user_level >= required_level
        except ValueError:
            return False
