# MedHelix — Complete Architecture Diagrams

## 1. 🏗️ Overall System Architecture

```mermaid
graph TB
    subgraph CLIENT["🏥 Client Layer (React 18 + TypeScript + Tailwind)"]
        UI_DASH["📊 Dashboard"]
        UI_CODING["💻 Coding Workspace"]
        UI_CLAIMS["📋 Claims Worklist"]
        UI_APPEALS["⚖️ Appeals Workspace"]
        UI_PAYMENTS["💰 Payments Workspace"]
        UI_HITL["👤 HITL Queue"]
        UI_ELIG["✅ Eligibility Check"]
        UI_REPORT["📈 Reporting"]
        UI_ASSIST["🤖 MedHelix Assistant"]
        UI_SETTINGS["⚙️ Settings"]
    end

    subgraph GATEWAY["🔐 API Gateway (FastAPI + Auth0 + RBAC)"]
        AUTH["Auth0 SSO/MFA"]
        RBAC["Role-Based Access Control"]
        RATE["Rate Limiting & Routing"]
    end

    subgraph MIG["🔌 MedHelix Integration Gateway (MIG)"]
        EHR_EPIC["EPIC\n(FHIR R4 / HL7)"]
        EHR_ECW["eClinicalWorks\n(FHIR / HL7)"]
        STEDI["Stedi Clearinghouse\n(837P/835/270/271/276/277/278)"]
        CLAUDE["Anthropic Claude\n(LLM API)"]
        NLP["AWS Comprehend Medical\n(Clinical NLP)"]
    end

    subgraph CORE["⚙️ Core Functional Modules (Python FastAPI)"]
        INTAKE["Intake &\nPre-Processing"]
        ELIG_MOD["Eligibility\nVerification"]
        PRIOR_AUTH["Prior\nAuthorization"]
        CODING["Intelligent\nCoding Engine"]
        CLAIM_SUB["Claim\nSubmission"]
        CLAIM_STATUS["Claim Status\nTracking"]
        PAYMENT["Payment\n& Posting"]
        DENIALS["Denials\nManagement"]
        APPEALS["Appeals\nManagement"]
        HITL["HITL\nQueue"]
        REPORTING["Reporting\n& Analytics"]
    end

    subgraph AI["🤖 AI & Intelligence Layer (LangGraph + LangChain)"]
        MWO["MedHelix Workflow\nOrchestrator (MWO)"]
        CCEA["CCEA\nExtraction Agent"]
        ICA["ICA\nCoding Agent"]
        CQAA["CQAA\nQuality Agent"]
        CRLA["CRLA\nLearning Agent"]
        ASSIST_AI["MedHelix\nAssistant AI"]
        PRB["Payer Rules\nBrain (PRB)"]
    end

    subgraph KNOWLEDGE["📚 Knowledge Services"]
        MCR["MCR\nMaster Code Repository\nICD-10 / CPT / HCPCS"]
        SCIE["SCIE\nSpecialty Compliance\nIntelligence Engine"]
        CLU["CLU\nClinical Language\nUnderstanding"]
    end

    subgraph INFRA["☁️ Infrastructure (AWS)"]
        PG["PostgreSQL 15+\nRow-Level Security\nMulti-Tenant"]
        REDIS["Redis Cache"]
        KAFKA["Kafka / RabbitMQ\nEvent Queue"]
        S3["AWS S3\nDocument Storage"]
        SECRETS["AWS Secrets\nManager"]
        EATS["EATS\nAudit Trail\nSystem"]
    end

    CLIENT --> GATEWAY
    GATEWAY --> CORE
    GATEWAY --> AI
    CORE --> MIG
    CORE --> AI
    CORE --> KNOWLEDGE
    CORE --> INFRA
    AI --> KNOWLEDGE
    AI --> INFRA
    MIG --> INFRA
```

---

## 2. 🔄 End-to-End RCM Claim Workflow

```mermaid
flowchart TD
    START([🏥 Patient Encounter]) --> INTAKE_NODE

    subgraph INTAKE_GRP["📥 Phase 1: Intake & Pre-Processing"]
        INTAKE_NODE["Encounter Ingestion\nEHR Data Pull\nEPIC / eClinicalWorks"] --> DEMO_VAL["Demographics\nValidation"]
        DEMO_VAL --> INS_DISC["Insurance\nDiscovery"]
        INS_DISC --> DOC_ING["Document\nIngestion"]
    end

    subgraph ELIG_GRP["✅ Phase 2: Eligibility Verification"]
        ELIG_CHECK["Real-time Eligibility\nEDI 270 Request"] --> ELIG_RESP["EDI 271 Response\nBenefits Display"]
        ELIG_RESP --> COV_VAL["Coverage\nValidation"]
    end

    subgraph PA_GRP["🔐 Phase 3: Prior Authorization"]
        PA_CHECK{"PA\nRequired?"} -->|Yes| PA_SUB["EDI 278\nSubmission"]
        PA_SUB --> PA_STATUS["PA Status\nTracking"]
        PA_CHECK -->|No| CODING_GRP
    end

    subgraph CODING_GRP["🧠 Phase 4: AI Intelligent Coding"]
        CCEA_NODE["CCEA Agent\nClinical Entity\nExtraction"] --> ICA_NODE["ICA Agent\nAI Code\nAssignment\nICD-10 / CPT"]
        ICA_NODE --> CQAA_NODE["CQAA Agent\nCoding Quality\n& Audit"]
        CQAA_NODE --> HITL_CHECK{"Confidence\nThreshold?"}
        HITL_CHECK -->|Low| HITL_NODE["HITL Queue\nHuman Review"]
        HITL_NODE --> CRLA_NODE["CRLA Agent\nLearning &\nFeedback Loop"]
        HITL_CHECK -->|High| CRLA_NODE
    end

    subgraph CLAIM_GRP["📋 Phase 5: Claim Submission"]
        PRB_NODE["Payer Rules Brain\nValidation\n+ Scrubbing"] --> EDI_837["837P Generation\nClaim Build"]
        EDI_837 --> STEDI_SUB["Stedi Clearinghouse\nSubmission"]
        STEDI_SUB --> ACK["Acknowledgment\nTracking"]
    end

    subgraph STATUS_GRP["📡 Phase 6: Claim Status"]
        EDI_276["EDI 276\nStatus Inquiry"] --> EDI_277["EDI 277\nStatus Response"]
        EDI_277 --> STATUS_DASH["Status Dashboard\n& Alerts"]
    end

    subgraph PAYMENT_GRP["💰 Phase 7: Payment & Posting"]
        ERA_835["ERA (835)\nIngestion"] --> AUTO_POST["Auto-Posting\nEngine"]
        AUTO_POST --> RECON["Reconciliation\n& Adjustments"]
        RECON --> EOB_PROC["EOB\nProcessing"]
    end

    subgraph DENIAL_GRP["🚫 Phase 8: Denials Management"]
        DENIAL_ING["Denial\nIngestion"] --> CARC_PARSE["CARC / RARC\nParsing"]
        CARC_PARSE --> ROOT_CAUSE["Root Cause\nAnalysis"]
        ROOT_CAUSE --> DENIAL_CAT["Denial\nCategorization"]
    end

    subgraph APPEALS_GRP["⚖️ Phase 9: Appeals Management"]
        APPEAL_GEN["AI Appeal Letter\nGeneration (Claude)"] --> APPEAL_SUB["Appeal\nSubmission"]
        APPEAL_SUB --> APPEAL_TRACK["Outcome\nTracking"]
    end

    DOC_ING --> ELIG_CHECK
    COV_VAL --> PA_CHECK
    PA_STATUS --> CODING_GRP
    CRLA_NODE --> PRB_NODE
    ACK --> EDI_276
    RECON --> DENIAL_CHECK{"Denied?"}
    DENIAL_CHECK -->|Yes| DENIAL_ING
    DENIAL_CHECK -->|No| SUCCESS([✅ Payment Complete])
    DENIAL_CAT --> APPEAL_CHECK{"Appeal\nWorthy?"}
    APPEAL_CHECK -->|Yes| APPEAL_GEN
    APPEAL_CHECK -->|No| WRITEOFF([📝 Write-off / AR])
    APPEAL_TRACK --> SUCCESS
```

---

## 3. 🤖 AI Coding Agents Pipeline (LangGraph)

```mermaid
stateDiagram-v2
    [*] --> CodingState

    state CodingState {
        [*] --> CCEA_AGENT
        note right of CCEA_AGENT
            Clinical Coding Extraction Agent
            - NLP Entity Extraction
            - Diagnoses, Procedures, Symptoms
            - Negation Detection
            - Temporal Reasoning
        end note

        CCEA_AGENT --> ICA_AGENT : extracted_entities

        note right of ICA_AGENT
            Intelligent Coding Agent
            - ICD-10 Code Assignment
            - CPT Code Assignment
            - HCPCS Code Assignment
            - Modifier Application
            - Confidence Scoring
        end note

        ICA_AGENT --> CQAA_AGENT : suggested_codes + scores

        note right of CQAA_AGENT
            Coding Quality & Audit Agent
            - NCCI Edit Check
            - MUE Limit Validation
            - Payer Rule Compliance
            - Bundling/Unbundling
            - LCD/NCD Compliance
        end note

        CQAA_AGENT --> ConfidenceCheck : validation_result

        state ConfidenceCheck <<choice>>
        ConfidenceCheck --> AUTO_APPROVE : confidence >= threshold
        ConfidenceCheck --> HITL_REVIEW : confidence < threshold

        HITL_REVIEW --> CRLA_AGENT : human_decision
        AUTO_APPROVE --> CRLA_AGENT : auto_approved

        note right of CRLA_AGENT
            Coding Review & Learning Agent
            - Feedback Loop Integration
            - Model Improvement
            - Payer Preference Learning
            - Outcome Tracking
        end note

        CRLA_AGENT --> [*] : final_codes
    }

    CodingState --> ClaimReady : finalized_codes
    ClaimReady --> [*]
```

---

## 4. 🏢 Multi-Tenant Architecture

```mermaid
graph TB
    subgraph PLATFORM["MedHelix Platform (Shared Infrastructure)"]

        subgraph SUPER_ADMIN["👑 Super Admin Layer"]
            SA["Super Admin\nCross-tenant Visibility\nPlatform Management"]
        end

        subgraph TENANT_A["🏥 Tenant A — Hospital Group"]
            TA_ADMIN["Tenant Admin"]
            TA_CODER["Coders"]
            TA_BILLER["Billers"]
            TA_VIEWER["Viewers"]
            TA_DB[("Tenant A\nDB Schema\nRow-Level Security")]
            TA_CONFIG["Payer Rules\nWorkflow Config\nBranding"]
        end

        subgraph TENANT_B["🏥 Tenant B — Private Practice"]
            TB_ADMIN["Tenant Admin"]
            TB_CODER["Coders"]
            TB_BILLER["Billers"]
            TB_DB[("Tenant B\nDB Schema\nRow-Level Security")]
            TB_CONFIG["Payer Rules\nWorkflow Config\nBranding"]
        end

        subgraph TENANT_N["🏥 Tenant N — RCM Billing Co."]
            TN_ADMIN["Tenant Admin"]
            TN_CODER["Coders"]
            TN_DB[("Tenant N\nDB Schema\nRow-Level Security")]
        end

        SHARED_AI["🤖 Shared AI Layer\nLangGraph Agents"]
        SHARED_KNOWLEDGE["📚 Shared Knowledge\nMCR / SCIE / CLU"]
        SHARED_INFRA["☁️ Shared Infrastructure\nAWS / PostgreSQL / Redis"]

    end

    SA --> TENANT_A
    SA --> TENANT_B
    SA --> TENANT_N
    TENANT_A --> SHARED_AI
    TENANT_B --> SHARED_AI
    TENANT_N --> SHARED_AI
    SHARED_AI --> SHARED_KNOWLEDGE
    SHARED_AI --> SHARED_INFRA
    TA_DB -.->|Isolated| TB_DB
    TB_DB -.->|Isolated| TN_DB
```

---

## 5. 📦 Module Dependency & Delivery Phases

```mermaid
gantt
    title MedHelix 12-Week Delivery Timeline
    dateFormat  YYYY-MM-DD
    section Track A
    Architecture & Infrastructure         :a1, 2026-05-01, 2w
    MIG (EPIC + eCW) & Intake             :a2, after a1, 3w
    Claim Submission (837P) + Status      :a3, after a2, 2w
    MedHelix Assistant + Dashboard        :a4, after a3, 2w

    section Track B
    Knowledge Services (MCR, SCIE, PRB, CLU) :b1, 2026-05-01, 2w
    Coding Agents (CCEA→ICA→CQAA→CRLA)   :b2, after b1, 3w
    ERA (835) + Payments + Denials        :b3, after b2, 2w
    Full UI Wiring + E2E Integration      :b4, after b3, 2w

    section Track C (Continuous)
    UI Refinement & Integration           :c1, 2026-05-01, 9w

    section All Tracks
    E2E Testing + Security + UAT + Go-Live :all1, 2026-07-03, 3w
```

---

## 6. 🔌 EDI Transaction Flow (Clearinghouse)

```mermaid
sequenceDiagram
    participant EHR as 🏥 EHR (EPIC/eCW)
    participant MIG as 🔌 MIG Gateway
    participant CORE as ⚙️ Core Engine
    participant STEDI as 📡 Stedi Clearinghouse
    participant PAYER as 🏦 Insurance Payer

    Note over EHR,PAYER: Eligibility Verification
    EHR->>MIG: Patient Encounter Data
    MIG->>CORE: Canonical Data Model
    CORE->>STEDI: EDI 270 (Eligibility Request)
    STEDI->>PAYER: Forward Request
    PAYER->>STEDI: Response
    STEDI->>CORE: EDI 271 (Eligibility Response)
    CORE->>MIG: Benefits & Coverage Data

    Note over EHR,PAYER: Claim Submission
    CORE->>STEDI: EDI 837P (Professional Claim)
    STEDI->>PAYER: Forward Claim
    STEDI->>CORE: EDI 999 (Acknowledgment)
    CORE->>STEDI: EDI 276 (Status Inquiry)
    STEDI->>CORE: EDI 277 (Claim Status)

    Note over EHR,PAYER: Payment Processing
    PAYER->>STEDI: EDI 835 (ERA Payment)
    STEDI->>CORE: ERA Ingestion
    CORE->>CORE: Auto-Posting & Reconciliation

    Note over EHR,PAYER: Prior Authorization
    CORE->>STEDI: EDI 278 (PA Request)
    STEDI->>PAYER: Forward PA Request
    PAYER->>STEDI: PA Decision
    STEDI->>CORE: EDI 278 Response
```
