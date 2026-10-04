from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Async Engine 
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,           # Log SQL queries in development
    pool_size=10,                  # Max 10 connections in pool
    max_overflow=20,               # Allow 20 extra connections under load
    pool_pre_ping=True,            # Verify connection is alive before use
    pool_recycle=3600,             # Recycle connections every 1 hour
)

#Session Factory 
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,        # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)

#Base Model 
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    All models inherit from this.
    """
    pass


#DB Dependency 
async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides a DB session per request.
    Automatically closes session when request is done.

    Usage in routes:
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


#Health Check 
async def check_db_connection() -> bool:
    """Verify database is reachable — used in /health endpoint"""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
