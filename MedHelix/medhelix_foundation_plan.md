# MedHelix — Foundation (Step 1) Plan

## 📌 Key Decision: What We Build NOW vs What Waits for Client

| Part | Build Now (Local) | Needs Client |
|------|------------------|--------------|
| FastAPI project structure | ✅ Yes | ❌ No |
| PostgreSQL (local Docker) | ✅ Yes | ❌ No |
| Redis (local Docker) | ✅ Yes | ❌ No |
| Multi-tenant DB schema | ✅ Yes | ❌ No |
| SQLAlchemy models | ✅ Yes | ❌ No |
| Pydantic schemas | ✅ Yes | ❌ No |
| API routes (all endpoints) | ✅ Yes | ❌ No |
| RBAC middleware | ✅ Yes | ❌ No |
| Audit trail (EATS) | ✅ Yes | ❌ No |
| LangGraph AI Agents | ✅ Yes | ❌ No |
| Auth0 SSO/MFA | ⏳ Placeholder | ✅ Auth0 keys |
| AWS RDS (Production DB) | ⏳ Use local PG | ✅ AWS access |
| AWS Secrets Manager | ⏳ Use .env locally | ✅ AWS access |
| AWS S3 (document storage) | ⏳ Use local folder | ✅ AWS access |
| Claude API (LLM) | ⏳ Need key | ✅ Claude API key |
| EPIC EHR integration | ⏳ Mock it | ✅ EPIC sandbox |
| eClinicalWorks integration | ⏳ Mock it | ✅ eCW sandbox |
| Stedi Clearinghouse | ⏳ Mock it | ✅ Stedi account |

---

## 📋 Client Requirements Checklist (Share This With Client)

### 🔑 Day 1 — Needed to Start AI Work
```
□ Anthropic Claude API Key
  → Used for: AI Coding Agents, MedHelix Assistant, Appeal Letters
  → Where: console.anthropic.com → API Keys

□ Auth0 Tenant Setup
  → Used for: SSO, MFA, multi-tenant authentication
  → Needs: Domain, Client ID, Client Secret, Audience
  → Where: auth0.com → Create Application (Machine to Machine)
```

### ☁️ Week 1-2 — Needed for Infrastructure
```
□ AWS Account Access (IAM User with these permissions)
  → EC2, RDS, ElastiCache, S3, Secrets Manager, KMS, VPC, IAM
  → Preferred: Create an IAM role for the dev team

□ AWS Region Decision (us-east-1 recommended for HIPAA)

□ AWS Services Required:
  → RDS PostgreSQL 15+ instance (or we use local Docker for dev)
  → ElastiCache Redis instance
  → S3 Bucket (for document storage, PHI encrypted)
  → Secrets Manager (for all API keys)
  → KMS Key (for encryption at rest)
  → VPC setup (private subnets for DB)
  → Route53 (for domain setup)
  → ACM Certificate (SSL/TLS)
  → CloudWatch (logging)
  → ECR (Docker image registry)
```

### 🏥 Week 3-5 — Needed for Integrations
```
□ EPIC Sandbox Credentials
  → Used for: Patient data, encounter ingestion
  → Needs: Client ID, Client Secret, Sandbox URL
  → Where: fhir.epic.com → Create App

□ eClinicalWorks Sandbox Credentials
  → Used for: Patient data, encounter ingestion
  → Needs: API Key, Sandbox URL, HL7 endpoint

□ Stedi Clearinghouse Account
  → Used for: EDI 837P, 835, 270/271, 276/277, 278
  → Where: stedi.com → Create account + API key
  → Needs: API Key, Trading Partner IDs

□ Payer Testing Credentials (optional but helpful)
  → Aetna, BCBS, UHC, Cigna, Humana sandbox access
  → For testing eligibility + claim submission
```

### 🔧 Optional but Good to Have
```
□ GitHub Organization (for repo access)
□ Jira/ClickUp project access
□ Slack workspace invite
□ Confluence/Notion space
□ Figma access (design files)
```

---

## 🏗️ Complete Project Folder Structure

```
medhelix-backend/
│
├── 📁 app/                          # Main application
│   │
│   ├── 📄 main.py                   # FastAPI app entry point
│   │
│   ├── 📁 core/                     # Core configuration
│   │   ├── config.py                # All env vars + settings
│   │   ├── database.py              # PostgreSQL connection (SQLAlchemy)
│   │   ├── redis.py                 # Redis connection
│   │   ├── security.py              # JWT + Auth0 validation
│   │   ├── dependencies.py          # FastAPI dependency injection
│   │   └── logging.py               # Structured logging setup
│   │
│   ├── 📁 middleware/               # Request middleware
│   │   ├── tenant.py                # Multi-tenant isolation
│   │   ├── rbac.py                  # Role-based access control
│   │   ├── audit.py                 # EATS - immutable audit trail
│   │   └── hipaa.py                 # HIPAA compliance checks
│   │
│   ├── 📁 models/                   # SQLAlchemy DB models
│   │   ├── base.py                  # Base model (tenant_id on all)
│   │   ├── tenant.py                # Tenant model
│   │   ├── user.py                  # User + roles
│   │   ├── patient.py               # Patient demographics
│   │   ├── encounter.py             # Clinical encounter
│   │   ├── claim.py                 # Claim lifecycle
│   │   ├── coding.py                # ICD-10/CPT code assignments
│   │   ├── eligibility.py           # Eligibility results
│   │   ├── prior_auth.py            # Prior authorization
│   │   ├── payment.py               # Payment + ERA posting
│   │   ├── denial.py                # Denial records
│   │   ├── appeal.py                # Appeal records
│   │   ├── hitl.py                  # HITL queue items
│   │   └── audit_log.py             # Immutable audit entries
│   │
│   ├── 📁 schemas/                  # Pydantic request/response schemas
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── encounter.py
│   │   ├── claim.py
│   │   ├── coding.py
│   │   ├── eligibility.py
│   │   ├── payment.py
│   │   ├── denial.py
│   │   ├── appeal.py
│   │   └── hitl.py
│   │
│   ├── 📁 api/                      # All API routes
│   │   └── 📁 v1/
│   │       ├── router.py            # Main v1 router
│   │       ├── auth.py              # Login, token, refresh
│   │       ├── dashboard.py         # KPIs, metrics, agent health
│   │       ├── intake.py            # Encounter intake queues
│   │       ├── coding.py            # Intelligent coding workspace
│   │       ├── claims.py            # Claims worklist + lifecycle
│   │       ├── eligibility.py       # Eligibility checks (270/271)
│   │       ├── prior_auth.py        # Prior auth (278)
│   │       ├── payments.py          # ERA (835) + posting OS
│   │       ├── denials.py           # Denial management
│   │       ├── appeals.py           # Appeals workspace
│   │       ├── hitl.py              # HITL review queue
│   │       ├── assistant.py         # MedHelix Assistant chat
│   │       ├── reporting.py         # Reports + analytics
│   │       ├── settings.py          # Tenant config, payers, users
│   │       └── admin.py             # Super admin endpoints
│   │
│   ├── 📁 services/                 # Business logic layer
│   │   ├── tenant_service.py        # Tenant CRUD + provisioning
│   │   ├── claim_service.py         # Claim lifecycle management
│   │   ├── coding_service.py        # Coding workflow orchestration
│   │   ├── eligibility_service.py   # Eligibility processing
│   │   ├── payment_service.py       # Payment posting logic
│   │   ├── denial_service.py        # Denial categorization
│   │   ├── appeal_service.py        # Appeal workflow
│   │   └── hitl_service.py          # HITL queue management
│   │
│   ├── 📁 agents/                   # 🤖 LangGraph AI Agents (YOUR WORK)
│   │   ├── state.py                 # CodingState TypedDict
│   │   ├── ccea_agent.py            # Clinical Coding Extraction Agent
│   │   ├── ica_agent.py             # Intelligent Coding Agent
│   │   ├── cqaa_agent.py            # Coding Quality & Audit Agent
│   │   ├── crla_agent.py            # Coding Review & Learning Agent
│   │   ├── coding_pipeline.py       # Full CCEA→ICA→CQAA→CRLA graph
│   │   ├── assistant_agent.py       # MedHelix Assistant (Tool Calling)
│   │   ├── denial_agent.py          # Denial analysis agent
│   │   ├── appeal_agent.py          # Appeal letter generation
│   │   └── tools/                   # Custom tool functions
│   │       ├── eligibility_tools.py
│   │       ├── coding_tools.py
│   │       ├── claim_tools.py
│   │       └── appeal_tools.py
│   │
│   ├── 📁 knowledge/                # Knowledge Services
│   │   ├── 📁 mcr/                  # Master Code Repository
│   │   │   ├── icd10.py             # ICD-10 lookup
│   │   │   ├── cpt.py               # CPT lookup
│   │   │   ├── hcpcs.py             # HCPCS lookup
│   │   │   ├── ncci.py              # NCCI edit rules
│   │   │   └── mue.py               # MUE limits
│   │   ├── 📁 prb/                  # Payer Rules Brain
│   │   │   ├── rules_engine.py      # Rule validation engine
│   │   │   ├── modifier_rules.py    # Modifier requirements
│   │   │   └── timely_filing.py     # Filing deadline rules
│   │   ├── 📁 scie/                 # Specialty Compliance Engine
│   │   │   ├── lcd_ncd.py           # LCD/NCD rules
│   │   │   ├── em_guidelines.py     # E/M documentation rules
│   │   │   └── hcc_mappings.py      # HCC code mappings
│   │   └── 📁 clu/                  # Clinical Language Understanding
│   │       ├── comprehend.py        # AWS Comprehend Medical wrapper
│   │       └── entity_extractor.py  # Entity extraction + normalization
│   │
│   └── 📁 integrations/             # MIG — External system connectors
│       ├── 📁 ehr/
│       │   ├── base.py              # Base EHR adapter
│       │   ├── epic.py              # EPIC FHIR R4 connector
│       │   └── ecw.py               # eClinicalWorks connector
│       └── 📁 clearinghouse/
│           ├── base.py              # Base EDI adapter
│           ├── stedi.py             # Stedi connector
│           └── edi/
│               ├── edi_270.py       # Eligibility request
│               ├── edi_271.py       # Eligibility response
│               ├── edi_278.py       # Prior auth
│               ├── edi_837p.py      # Professional claim
│               ├── edi_835.py       # ERA payment
│               ├── edi_276.py       # Claim status request
│               └── edi_277.py       # Claim status response
│
├── 📁 migrations/                   # Alembic DB migrations
│   ├── env.py
│   └── versions/
│       └── 001_initial_schema.py
│
├── 📁 tests/                        # Test suite
│   ├── 📁 unit/
│   │   ├── test_agents.py
│   │   ├── test_services.py
│   │   └── test_knowledge.py
│   ├── 📁 integration/
│   │   ├── test_api_auth.py
│   │   ├── test_api_claims.py
│   │   └── test_api_coding.py
│   └── conftest.py
│
├── 📁 infra/                        # AWS Infrastructure (Terraform)
│   ├── main.tf
│   ├── vpc.tf
│   ├── rds.tf                       # PostgreSQL RDS
│   ├── elasticache.tf               # Redis
│   ├── s3.tf                        # Document storage
│   ├── kms.tf                       # Encryption keys
│   ├── secrets.tf                   # Secrets Manager
│   └── variables.tf
│
├── 📁 docker/                       # Local development
│   ├── Dockerfile
│   └── docker-compose.yml           # PG + Redis + API locally
│
├── 📁 scripts/                      # Utility scripts
│   ├── seed_mcr.py                  # Load ICD-10/CPT data
│   ├── seed_tenants.py              # Create sample tenants
│   └── seed_sample_data.py          # Sample patients/claims
│
├── 📄 .env.example                  # Template (commit this)
├── 📄 .env                          # Actual secrets (gitignored!)
├── 📄 .gitignore
├── 📄 requirements.txt
├── 📄 alembic.ini
├── 📄 Makefile                      # Shortcuts: make dev, make test
└── 📄 README.md
```

---

## 🐳 Local Dev Setup (Without AWS — Using Docker)

```yaml
# docker-compose.yml — Run this locally while client provides AWS

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: medhelix
      POSTGRES_USER: medhelix
      POSTGRES_PASSWORD: localpassword
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://medhelix:localpassword@postgres:5432/medhelix
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
```

---

## 🔒 Environment Variables (.env.example)

```bash
# ── Database ────────────────────────────────────────────
DATABASE_URL=postgresql://medhelix:password@localhost:5432/medhelix
# → LOCAL: Docker PostgreSQL
# → PRODUCTION: Client provides AWS RDS endpoint

# ── Redis ───────────────────────────────────────────────
REDIS_URL=redis://localhost:6379
# → LOCAL: Docker Redis
# → PRODUCTION: Client provides AWS ElastiCache endpoint

# ── Auth0 (SSO) ─────────────────────────────────────────
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_CLIENT_ID=xxxxx
AUTH0_CLIENT_SECRET=xxxxx
AUTH0_AUDIENCE=https://api.medhelix.com
# → Client provides from auth0.com

# ── AI / LLM ────────────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-xxxxx
# → Client provides from console.anthropic.com

# ── AWS ─────────────────────────────────────────────────
AWS_ACCESS_KEY_ID=xxxxx           # Client provides
AWS_SECRET_ACCESS_KEY=xxxxx       # Client provides
AWS_REGION=us-east-1              # Client decides
AWS_S3_BUCKET=medhelix-documents  # Client creates

# ── EHR Integrations ────────────────────────────────────
EPIC_CLIENT_ID=xxxxx              # Client provides
EPIC_CLIENT_SECRET=xxxxx          # Client provides
EPIC_SANDBOX_URL=https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4

ECW_API_KEY=xxxxx                 # Client provides
ECW_BASE_URL=xxxxx                # Client provides

# ── Clearinghouse ───────────────────────────────────────
STEDI_API_KEY=xxxxx               # Client provides

# ── App Settings ────────────────────────────────────────
APP_ENV=development               # development | staging | production
SECRET_KEY=your-jwt-secret        # Generate: openssl rand -hex 32
DEBUG=True
```

---

## 🚦 What We Build This Week (Without AWS)

### Day 1-2: Project Skeleton
```
✅ Create medhelix-backend/ folder structure
✅ Setup FastAPI with app/main.py
✅ Setup docker-compose.yml (PG + Redis)
✅ Install dependencies (requirements.txt)
✅ Setup Alembic for migrations
✅ Create .env.example
```

### Day 3-4: Multi-Tenant DB Schema
```
✅ models/base.py          (tenant_id on EVERY table)
✅ models/tenant.py        (Tenant model)
✅ models/user.py          (User + RBAC roles)
✅ migrations/001_initial  (First Alembic migration)
✅ Test: Create 2 tenants, verify data isolation
```

### Day 5-7: Core Models + API Skeleton
```
✅ All SQLAlchemy models (patient, encounter, claim, etc.)
✅ All Pydantic schemas
✅ API route files (empty handlers returning mock data)
✅ RBAC middleware (local JWT, no Auth0 yet)
✅ Audit trail middleware (EATS)
```

### Parallel: Knowledge Services
```
✅ Load ICD-10 codes into MCR table (public data, no AWS needed)
✅ Load CPT codes
✅ Build fast lookup API (Redis cached)
✅ Test: lookup("pneumonia") → returns J18.9
```

---

## 📞 What to Tell the Client Right Now

```
Please provide the following by Day 1:
1. ✅ Anthropic Claude API key (for AI agents)
2. ✅ Auth0 tenant setup (domain + credentials)

Please provide by Week 2:
3. ✅ AWS IAM credentials (dev environment)
4. ✅ GitHub organization + repository access

Please provide by Week 3:
5. ✅ EPIC sandbox credentials
6. ✅ eClinicalWorks sandbox credentials
7. ✅ Stedi clearinghouse account + API key

Optional but helpful:
8. ✅ Jira/ClickUp project access
9. ✅ Slack channel invite
```
