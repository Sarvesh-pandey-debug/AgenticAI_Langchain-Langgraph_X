from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from app.core.config import settings
from app.core.database import check_db_connection
from app.core.redis import get_redis, close_redis, check_redis_connection
from app.api.v1.router import api_router

#Logging Setup 
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# Lifespan (Startup + Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events.
    - Startup: Initialize Redis, verify DB connection
    - Shutdown: Close Redis connection cleanly
    """
    #STARTUP
    logger.info("MedHelix API starting up...")

    # Initialize Redis connection
    await get_redis()
    logger.info("Redis connected")

    # Verify DB is reachable
    db_ok = await check_db_connection()
    if db_ok:
        logger.info("PostgreSQL connected")
    else:
        logger.error("PostgreSQL connection failed — check DATABASE_URL")

    logger.info(f"MedHelix {settings.APP_VERSION} running in [{settings.APP_ENV}] mode")

    yield  # App runs here

    #SHUTDOWN
    logger.info("MedHelix API shutting down...")
    await close_redis()
    logger.info("Redis connection closed")


#FastAPI App 
app = FastAPI(
    title="MedHelix API",
    description=(
        "AI-powered Revenue Cycle Management platform. "
        "HIPAA-compliant, multi-tenant, agentic AI workflows."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan,
)


#CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Request Timing Middleware 
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Adds X-Process-Time header to every response"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2)) + "ms"
    return response


#Global Exception Handler 
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "Something went wrong",
        },
    )


#Health Check Endpoint 
@app.get("/health", tags=["System"])
async def health_check():
    """
    System health check — verifies all critical dependencies.
    Used by Docker healthcheck and load balancer probes.
    """
    db_healthy = await check_db_connection()
    redis_healthy = await check_redis_connection()

    all_healthy = db_healthy and redis_healthy

    return JSONResponse(
        status_code=status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "healthy" if all_healthy else "degraded",
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "services": {
                "database": " connected" if db_healthy else " unreachable",
                "redis": " connected" if redis_healthy else " unreachable",
            },
        },
    )


#Root Endpoint 
@app.get("/", tags=["System"])
async def root():
    return {
        "message": "MedHelix AI-Powered RCM Platform",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


# Include API Router 
app.include_router(api_router, prefix="/api/v1")
