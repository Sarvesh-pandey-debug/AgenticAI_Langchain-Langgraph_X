# MedHelix — API Documentation

This document lists all the API routes that have been created and registered in the FastAPI application.

> **Note**: You can always view the interactive Swagger API documentation locally by opening your browser and visiting: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🟢 System Level Endpoints
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/` | Root endpoint, returns app version | ✅ Live |
| `GET` | `/health` | Deep health check (PostgreSQL + Redis) | ✅ Live |

---

## 🏥 V1 API Endpoints (`/api/v1/...`)
Currently, these are "mock" router endpoints. The files exist in `app/api/v1/` but simply return a basic message. We will fill them with actual business logic soon.

### Authentication & Access
| Method | Endpoint | File Location |
|--------|----------|---------------|
| `GET` | `/api/v1/auth/` | `app/api/v1/auth.py` |
| `GET` | `/api/v1/admin/` | `app/api/v1/admin.py` |
| `GET` | `/api/v1/settings/` | `app/api/v1/settings.py` |

### Core RCM Workflow
| Method | Endpoint | File Location |
|--------|----------|---------------|
| `GET` | `/api/v1/intake/` | `app/api/v1/intake.py` |
| `GET` | `/api/v1/eligibility/` | `app/api/v1/eligibility.py` |
| `GET` | `/api/v1/prior-auth/` | `app/api/v1/prior_auth.py` |
| `GET` | `/api/v1/coding/` | `app/api/v1/coding.py` |
| `GET` | `/api/v1/claims/` | `app/api/v1/claims.py` |
| `GET` | `/api/v1/payments/` | `app/api/v1/payments.py` |
| `GET` | `/api/v1/denials/` | `app/api/v1/denials.py` |
| `GET` | `/api/v1/appeals/` | `app/api/v1/appeals.py` |

### Dashboards & Human-In-The-Loop
| Method | Endpoint | File Location |
|--------|----------|---------------|
| `GET` | `/api/v1/dashboard/` | `app/api/v1/dashboard.py` |
| `GET` | `/api/v1/hitl/` | `app/api/v1/hitl.py` |
| `GET` | `/api/v1/reporting/` | `app/api/v1/reporting.py` |

### AI Assistant
| Method | Endpoint | File Location |
|--------|----------|---------------|
| `GET` | `/api/v1/assistant/` | `app/api/v1/assistant.py` |
