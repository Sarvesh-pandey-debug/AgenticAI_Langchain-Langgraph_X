from fastapi import APIRouter

# ── Import all route modules ───────────────────────────────────────
from app.api.v1 import (
    auth,
    dashboard,
    intake,
    coding,
    claims,
    eligibility,
    prior_auth,
    payments,
    denials,
    appeals,
    hitl,
    assistant,
    reporting,
    settings as settings_router,
    admin,
)

# ── Main v1 Router ────────────────────────────────────────────────
api_router = APIRouter()

# ── Register all sub-routers ──────────────────────────────────────
api_router.include_router(auth.router,            prefix="/auth",        tags=["Authentication"])
api_router.include_router(dashboard.router,       prefix="/dashboard",   tags=["Dashboard"])
api_router.include_router(intake.router,          prefix="/intake",      tags=["Intake"])
api_router.include_router(coding.router,          prefix="/coding",      tags=["Intelligent Coding"])
api_router.include_router(claims.router,          prefix="/claims",      tags=["Claims"])
api_router.include_router(eligibility.router,     prefix="/eligibility", tags=["Eligibility"])
api_router.include_router(prior_auth.router,      prefix="/prior-auth",  tags=["Prior Authorization"])
api_router.include_router(payments.router,        prefix="/payments",    tags=["Payments"])
api_router.include_router(denials.router,         prefix="/denials",     tags=["Denials"])
api_router.include_router(appeals.router,         prefix="/appeals",     tags=["Appeals"])
api_router.include_router(hitl.router,            prefix="/hitl",        tags=["HITL Queue"])
api_router.include_router(assistant.router,       prefix="/assistant",   tags=["MedHelix Assistant"])
api_router.include_router(reporting.router,       prefix="/reporting",   tags=["Reporting"])
api_router.include_router(settings_router.router, prefix="/settings",    tags=["Settings"])
api_router.include_router(admin.router,           prefix="/admin",       tags=["Super Admin"])
