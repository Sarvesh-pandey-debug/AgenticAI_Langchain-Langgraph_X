# MedHelix P0 — Where to Start & Build Sequence

## 🧠 The Golden Rule
> **Never build a module that depends on something you haven't built yet.**
> Foundation → Knowledge → AI Agents → Integrations → Core Modules → Assistant

---

## 📊 Dependency Map (P0 Only)

```
FOUNDATION (DB + FastAPI + Auth)
        ↓
KNOWLEDGE SERVICES (MCR + PRB + CLU + SCIE)
        ↓
AI CODING AGENTS (CCEA → ICA → CQAA → CRLA)  ←── Your LangGraph Work
        ↓
MIG INTEGRATIONS (EHR + Clearinghouse)
        ↓
CORE MODULES (Intake → Eligibility → Coding → Claim → Payment → Denials → Appeals)
        ↓
MEDHELIX ASSISTANT + HITL + REPORTING
        ↓
UI WIRING + E2E TESTING
```

---

## 🏁 STEP 1 — Project Foundation
> ⏱️ Week 1–2 | Track A | Pure Backend Setup

### What to build:
- [ ] FastAPI project structure (Monorepo with Turborepo)
- [ ] PostgreSQL 15+ setup with **row-level multi-tenant isolation**
- [ ] Redis cache setup
- [ ] Auth0 integration (SSO + MFA)
- [ ] RBAC middleware (Super Admin, Tenant Admin, Coder, Biller, Viewer)
- [ ] AWS infrastructure (VPC, KMS, Secrets Manager)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Dev / Staging / Production environments

### Why first?
> Everything else (AI agents, modules, integrations) needs the DB schema,
> auth system, and project structure to exist first.
> You can't store agent results without a DB. You can't call APIs without auth.

### Your starting file structure:
```
medhelix/
├── apps/
│   ├── api/              ← FastAPI backend
│   └── web/              ← React frontend (already built)
├── packages/
│   ├── db/               ← PostgreSQL models (SQLAlchemy)
│   ├── agents/           ← LangGraph agents ← YOUR MAIN WORK
│   ├── knowledge/        ← MCR, PRB, CLU, SCIE
│   └── integrations/     ← MIG (EHR + Clearinghouse)
├── infra/                ← Terraform / AWS IaC
└── .env
```

---

## 📚 STEP 2 — Knowledge Services
> ⏱️ Week 1–2 | Track B | Parallel with Step 1

### What to build:
- [ ] **MCR** — Master Code Repository
  - Load ICD-10 codes into PostgreSQL
  - Load CPT codes
  - Load HCPCS codes
  - NCCI edit rules
  - MUE limits
  - Fast lookup APIs (Redis cached)

- [ ] **PRB** — Payer Rules Brain
  - Payer-specific billing rules DB
  - Modifier rules per payer
  - Timely filing limits
  - Prior auth requirement flags
  - Rule validation engine

- [ ] **CLU** — Clinical Language Understanding
  - AWS Comprehend Medical integration
  - Entity extraction API (diagnoses, procedures, medications)
  - Negation detection
  - Temporal reasoning

- [ ] **SCIE** — Specialty Compliance Intelligence Engine
  - LCD/NCD rules (Internal Medicine + Family Practice for P0)
  - E/M guidelines
  - HCC mappings

### Why second?
> Your AI agents (CCEA, ICA, CQAA) are useless without these.
> CCEA needs CLU. ICA needs MCR. CQAA needs PRB and SCIE.
> These are the DATA BRAIN your agents query.

---

## 🤖 STEP 3 — AI Coding Agents (LangGraph) ← YOUR CORE WORK
> ⏱️ Week 3–5 | Track B | This is your LangGraph expertise!

### What to build:
This is a **sequential LangGraph pipeline** — exactly like your blog generator,
but for medical coding.

```
START → CCEA → ICA → CQAA → [HITL or AUTO] → CRLA → END
```

#### State Definition:
```python
class CodingState(TypedDict):
    # Input
    clinical_note: str
    patient_id: str
    encounter_id: str
    specialty: str
    payer_id: str

    # CCEA Output
    extracted_entities: list      # diagnoses, procedures, symptoms
    negated_entities: list        # what patient does NOT have
    temporal_info: dict           # onset, duration, etc.

    # ICA Output
    suggested_icd10: list         # [{"code": "J18.9", "confidence": 0.95}]
    suggested_cpt: list           # [{"code": "99213", "confidence": 0.88}]
    modifiers: list               # ["25", "59"]

    # CQAA Output
    validation_result: str        # "PASS" or "FAIL"
    ncci_edits: list              # any bundling issues
    payer_rule_flags: list        # payer-specific issues
    confidence_score: float       # 0.0 to 1.0

    # CRLA Output
    final_codes: list             # Approved final codes
    hitl_required: bool           # Needs human review?
    audit_trail: list             # Full decision log
```

#### The 4 Agents:

**CCEA — Clinical Coding Extraction Agent**
- Tool: AWS Comprehend Medical (CLU)
- Extracts: diagnoses, procedures, medications, symptoms
- Handles: negation ("no fever"), temporality ("3 days ago")

**ICA — Intelligent Coding Agent**
- Tool: MCR lookup (ICD-10, CPT, HCPCS)
- Tool: Claude LLM for reasoning
- Output: suggested codes with confidence scores

**CQAA — Coding Quality & Audit Agent**
- Tool: PRB (payer rules validation)
- Tool: NCCI edit checks
- Tool: MUE limit validation
- Output: PASS/FAIL + flags

**CRLA — Coding Review & Learning Agent**
- Collects HITL decisions
- Updates learning DB
- Improves future confidence scores

### Why third?
> This is the heart of MedHelix's AI value.
> Can be built and tested BEFORE integrations are ready.
> You can test with sample clinical notes without needing real EHR data.

---

## 🔌 STEP 4 — MedHelix Integration Gateway (MIG)
> ⏱️ Week 3–5 | Track A | Integration Work

### What to build (P0 only):
- [ ] **EPIC Integration** — FHIR R4 / HL7 adapter
- [ ] **eClinicalWorks Integration** — FHIR / HL7 adapter
- [ ] **Canonical Data Model** — Normalize EHR data to standard schema
- [ ] **Stedi Clearinghouse** — EDI transaction support:
  - EDI 270/271 (Eligibility)
  - EDI 837P (Claim Submission)
  - EDI 835 (ERA/Payment)
  - EDI 276/277 (Claim Status)
  - EDI 278 (Prior Authorization)

### Why fourth?
> You need Step 1 (DB + auth) to store the data.
> You need Step 2 (canonical schema) to normalize EHR data.
> Steps 1 and 2 don't depend on MIG, so MIG can run parallel.

---

## ⚙️ STEP 5 — Core Functional Modules
> ⏱️ Week 6–9 | All Tracks | Wires everything together

### Build order within Step 5:
```
1. Intake & Pre-Processing      (needs MIG + DB)
2. Eligibility Verification     (needs MIG + EDI 270/271)
3. Prior Authorization          (needs MIG + EDI 278)
4. Intelligent Coding           (needs AI Agents + MIG data)
5. Claim Submission             (needs Coding + EDI 837P)
6. Claim Status Tracking        (needs EDI 276/277)
7. Payment & Posting            (needs EDI 835)
8. Denials Management           (needs Payment data + PRB)
9. Appeals Management           (needs Denials + Claude)
10. HITL Queue                  (needs Coding + Denials)
11. Reporting & Analytics       (needs all modules)
```

### Why fifth?
> Each module wraps around the integrations and agents built earlier.
> They're the business logic glue between MIG + AI Agents + DB.

---

## 🤖 STEP 6 — MedHelix Assistant + HITL + Dashboard
> ⏱️ Week 8–9 | Track A | Tool Calling Agent

### What to build:
- [ ] **MedHelix Assistant** — ReAct Tool Calling Agent (LangGraph)
  - Custom tools: eligibility check, claim status, code lookup, appeal generator
  - Conversational UI (slide-out panel, already in frontend)

- [ ] **HITL Queue** — Human-in-the-loop workflow
  - Review queue for low-confidence coding decisions
  - Approve/reject with feedback to CRLA

- [ ] **Dashboard & Reporting**
  - KPIs: clean claim rate, denial rate, avg payment time
  - Denial trend charts
  - AR aging buckets

### Why last?
> MedHelix Assistant calls tools from ALL previous modules.
> Dashboard needs data from ALL modules to display metrics.
> HITL needs the Coding Agent output to review.

---

## 🎯 Quick Summary — Your Build Order

| Step | What | Week | Your Role |
|------|------|------|-----------|
| **1** | Foundation (FastAPI + DB + Auth + AWS) | W1-2 | Setup |
| **2** | Knowledge Services (MCR + PRB + CLU + SCIE) | W1-2 | Data Layer |
| **3** | 🔥 AI Coding Agents (CCEA→ICA→CQAA→CRLA) | W3-5 | **LangGraph** |
| **4** | MIG (EPIC + eCW + Stedi EDI) | W3-5 | Integrations |
| **5** | Core Modules (Intake→Eligibility→Coding→Claims→Payment→Denials→Appeals) | W6-9 | Business Logic |
| **6** | 🔥 MedHelix Assistant + HITL + Dashboard | W8-9 | **Tool Calling** |
| **7** | UI Wiring + E2E Testing + UAT + Go-Live | W10-12 | Final Polish |

---

## 🚀 Where to Start RIGHT NOW (Day 1)

> If you're starting today, do these in order:

1. ✅ Create FastAPI project structure
2. ✅ Design the PostgreSQL multi-tenant schema (most critical decision)
3. ✅ Set up `.env` with Claude API key, DB URL, Redis URL
4. ✅ Create MCR tables and load sample ICD-10 / CPT data
5. ✅ Build your first LangGraph agent — **CCEA** (test with a sample clinical note)

> The CCEA agent can be built and tested on Day 1 with zero integrations!
> Just pass in a clinical note string and get extracted entities back.

---

## ⚠️ What NOT to Start With (Common Mistake)

| Don't Start With | Why |
|-----------------|-----|
| EHR Integration (EPIC) | Needs sandbox credentials + complex setup |
| Clearinghouse (Stedi) | Needs test accounts, EDI knowledge |
| Frontend wiring | Frontend is already built; wire it last |
| Reporting dashboard | Nothing to report if modules aren't built |
| Denial prediction ML | This is P1, not P0 |
