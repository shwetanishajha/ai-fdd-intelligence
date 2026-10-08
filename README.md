# AI-FDD Intelligence

Evidence-backed AI platform for Financial Due Diligence (FDD).

AI-FDD Intelligence combines deterministic financial analysis, RAG-based evidence retrieval, specialist AI agents, controlled agent orchestration, structured validation and human review to accelerate financial due diligence.

> **Prototype:** This project uses synthetic financial data and is designed to demonstrate enterprise AI architecture and engineering patterns.

---

## 1. What the Platform Does

The platform supports two primary workflows:

### Generate Full FDD

A user can initiate a complete FDD analysis.

```text
Generate FDD
     ↓
FDD Orchestrator
     ↓
Specialist Agents
     ↓
Evidence + Financial Analysis
     ↓
Report Synthesis
     ↓
Validation
     ↓
FDD Report

Ask an FDD Question
A user can ask a targeted question about the deal.
User Question
     ↓
AI Planner
     ↓
Select Required Agents
     ↓
Controlled Agent Execution
     ↓
Evidence-backed Answer

2. Architecture
                         ┌─────────────────────┐
                         │     FDD User / UI   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │       FDD API       │
                         │ Generate / Query /   │
                         │ Human Review         │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │  FDD Orchestrator   │
                         └───────┬───────┬──────┘
                                 │       │
                         Generate│       │Query
                                 │       │
              ┌──────────────────▼─┐   ┌─▼────────────────┐
              │ Specialist Agents   │   │   AI Planner     │
              │                     │   │                  │
              │ Revenue             │   │ Select required  │
              │ EBITDA              │   │ specialist       │
              │ Working Capital     │   │ agents           │
              │ Customer Risk       │   └────────┬─────────┘
              │ Financial Anomaly   │            │
              └──────────┬──────────┘            │
                         └──────────┬─────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │   Validation Layer  │
                         │                     │
                         │ Pydantic validation │
                         │ Deterministic calc  │
                         │ Evidence validation │
                         └──────────┬──────────┘
                                    ▼
                         ┌─────────────────────┐
                         │  Report Synthesis   │
                         │  + Evidence Register│
                         └──────────┬──────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    Human Review     │
                         │ Approve / Amend /   │
                         │ Reject              │
                         └──────────┬──────────┘
                                    ▼
                         ┌─────────────────────┐
                         │ FDD Report / Answer │
                         └─────────────────────┘

                         Detailed architecture is documented in:
- architecture/architecture.md
- architecture/adr.md
- architecture/evaluation.md

3. Key Architectural Principles
Deterministic before probabilistic
Financial calculations are performed using deterministic Python logic.
Examples:
- Revenue growth
- EBITDA margin
- Working capital movement
- Customer concentration
LLMs are used for interpretation, reasoning and synthesis rather than being treated as the source of truth for financial arithmetic.
RAG for deal-specific knowledge
Deal documents are ingested, chunked, embedded and indexed for semantic retrieval.
Retrieved evidence retains source and page information to support provenance.
LLM proposes; application authorizes; code executes
The AI planner can recommend specialist agents.
The application validates the proposed agents against an explicit allow-list and registry before execution.
LLM Planner
    ↓
Proposed Agents
    ↓
Allow-list Validation
    ↓
Agent Registry
    ↓
Controlled Execution

Human-in-the-loop
FDD findings can be:
- Approved
- Amended
- Rejected
This keeps consequential financial conclusions subject to human accountability.
4. Specialist Agents
The current platform contains five specialist agents:
Agent	Responsibility
Revenue Agent	Revenue movement and growth
EBITDA Agent	EBITDA and margin analysis
Working Capital Agent	Working capital movements
Customer Concentration Agent	Customer concentration risk
Financial Anomaly Agent	Unusual financial movements


The architecture is intentionally modular so additional FDD capabilities can be added without redesigning the complete workflow.
5. AI / Retrieval Architecture
PDF Documents
     ↓
PDF Loader
     ↓
Text Chunking
     ↓
Embeddings
     ↓
Vector Store
     ↓
Semantic Retrieval
     ↓
Evidence
     ↓
AI Agent
     ↓
Structured Finding

Documents are treated as untrusted data.
Retrieved content is evidence, not system instructions.
This creates an explicit trust boundary between external documents and AI reasoning.
6. Security Controls
The prototype addresses several AI-specific risks.
Prompt Injection
Retrieved documents are treated as untrusted content.
The system uses:
- evidence-only prompting
- structured output validation
- controlled agent execution
- provenance
- human review
Unauthorized Agent Execution
The planner cannot execute arbitrary agents.
Agent execution is restricted through:
Allowed Agent Set
       ↓
Agent Registry
       ↓
Validated Execution

Unsupported AI Output
Pydantic models validate structured AI responses before the application accepts them.
Financial Calculation Risk
Critical financial calculations are performed deterministically rather than delegated to the LLM.
Credential Protection
API credentials are loaded through environment configuration and excluded from source control.
See:
docs/threat-model.md
7. Centralised LLM Service
Generative AI calls are routed through:
src/core/llm_client.py

The service provides a common boundary for:
- model configuration
- timeout
- retry behaviour
- safe failure
Architecture:
AI Agents
    ↓
LLM Service
    ├── Timeout
    ├── Retry
    ├── Model Configuration
    └── Safe Failure
         ↓
       LLM API

The design provides a natural extension point for a future multi-model routing layer.
8. Human Review
The review workflow is:
AI Finding
    ↓
Human Review
    ├── Approve
    ├── Amend
    └── Reject

Review state is retained as part of the validated finding.
9. Evaluation
The project includes an evaluation framework covering:
- Retrieval relevance
- Evidence correctness
- Citation correctness
- Calculation accuracy
- Groundedness
- Planner behaviour
- Agent execution
- Prompt injection scenarios
- Human review
Current baseline:
Evidence evaluation: 5/5 passed
Planner evaluations: Passed
Full automated test suite: 50 passed

Evaluation assets are located in:
evaluation/

Detailed evaluation architecture:
architecture/evaluation.md
10. Project Structure
ai-fdd-intelligence/
│
├── architecture/
│   ├── architecture.md
│   ├── adr.md
│   └── evaluation.md
│
├── data/
│   ├── financials/
│   └── company_profile.md
│
├── docs/
│   └── threat-model.md
│
├── evaluation/
│   ├── questions.json
│   ├── planner_questions.json
│   ├── agentic_questions.json
│   ├── evaluation_criteria.json
│   ├── run_evaluation.py
│   ├── run_planner_evaluation.py
│   └── run_agentic_evaluation.py
│
├── src/
│   ├── agents/
│   │   ├── fdd_analyzer.py
│   │   ├── planner.py
│   │   ├── executor.py
│   │   ├── registry.py
│   │   ├── agentic_fdd.py
│   │   ├── fdd_product.py
│   │   ├── report_agent.py
│   │   └── ...
│   │
│   ├── api/
│   │   └── main.py
│   │
│   ├── core/
│   │   └── llm_client.py
│   │
│   ├── ingestion/
│   ├── retrieval/
│   ├── reporting/
│   └── validation/
│
├── tests/
│
├── .env
├── .gitignore
└── README.md

11. API
Health
GET /health

Generate FDD
POST /fdd/generate

Generates a complete FDD analysis and report.
Ask FDD Question
POST /fdd/query?question=<question>

Returns an evidence-backed answer using the agentic workflow.
Human Review
POST /fdd/review

Supports:
- Approved
- Amended
- Rejected
12. Running the Project
Create the virtual environment:
py -m venv .venv

Install dependencies:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Configure the OpenAI API key in .env:
OPENAI_API_KEY=your_api_key

Do not commit .env.
13. Run Tests
.\.venv\Scripts\python.exe -m pytest -q

Current test baseline:
50 passed

14. Generate an FDD Report
.\.venv\Scripts\python.exe -c "from src.agents.fdd_product import run_fdd; r=run_fdd('generate'); print(r['pdf_path'])"

The generated report is written to:
data/fdd_report_generated.pdf

15. Run the API
.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload

The API can then be accessed through the local FastAPI service.
16. Example FDD Questions
Examples:
What is the main customer concentration risk?

What was the FY2025 EBITDA margin?

How did working capital change from FY2024 to FY2025?

What are the key financial risks?

17. Production Evolution
This project intentionally focuses on demonstrating the core AI and architecture patterns rather than building a full production platform.
A production implementation could evolve toward:
Enterprise Identity / RBAC
          ↓
Secure API Gateway
          ↓
Stateless FDD Services
          ↓
Async Orchestration
          ↓
Specialist Agent Workers
          ↓
Managed Data / Vector Store
          ↓
Model Gateway
          ↓
Observability / Audit

Additional production capabilities would include:
- authentication and authorization
- tenant isolation
- secure document storage
- managed vector infrastructure
- asynchronous processing
- model fallback
- centralized observability
- audit logging
- secrets management
- cost controls
- resilience and disaster recovery
18. Architectural Trade-offs
RAG vs Fine-tuning
RAG was selected because FDD knowledge changes by transaction and evidence provenance is important.
Multi-agent vs Single-agent
Specialist agents provide separation of responsibility, independent testing and controlled execution at the cost of additional orchestration complexity.
LLM vs Deterministic Logic
LLMs are used for reasoning and synthesis.
Deterministic code is used for financial calculations and application controls.
Human vs Fully Autonomous Decision Making
The platform intentionally retains human review for consequential conclusions rather than treating AI output as automatically authoritative.
19. Key Engineering Principle
The platform separates:
Deterministic computation
        +
Evidence retrieval
        +
Probabilistic reasoning
        +
Human judgement

The goal is not to make the LLM responsible for everything.
The goal is to use AI where it provides value while maintaining deterministic controls around financial computation, execution, validation, provenance and human accountability.
20. Status
Completed
- [x] PDF document ingestion
- [x] Chunking and embeddings
- [x] Vector retrieval
- [x] Financial metric validation
- [x] Specialist FDD agents
- [x] AI planner
- [x] Controlled agent registry
- [x] Agent executor
- [x] Agentic FDD workflow
- [x] Executive summary
- [x] Report synthesis
- [x] PDF report generation
- [x] Evidence provenance
- [x] Human review
- [x] Prompt injection testing
- [x] Evaluation framework
- [x] Centralised LLM service
- [x] Architecture documentation
- [x] ADRs
- [x] Evaluation architecture
- [x] 50 automated tests passing
Future
- [ ] Interactive web UI
- [ ] Enterprise authentication/RBAC
- [ ] Multi-tenant architecture
- [ ] Async job orchestration
- [ ] Model routing
- [ ] Production observability
- [ ] Managed cloud deployment
21. Disclaimer
This repository uses synthetic company and financial data.
It is a technology demonstration and is not intended to provide actual investment, financial, accounting or transaction advice.