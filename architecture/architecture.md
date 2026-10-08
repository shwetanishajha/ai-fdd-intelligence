# AI-FDD Intelligence — Architecture

## 1. Purpose

AI-FDD Intelligence is an evidence-backed AI platform for financial due diligence.

The platform supports two primary business capabilities:

1. Generate a complete Financial Due Diligence report.
2. Answer specific FDD questions using evidence from the supplied deal documents.

The architecture separates deterministic financial computation, retrieval, probabilistic AI reasoning, orchestration, validation, and human judgement.

---

## 2. High-Level Architecture

```text
                         ┌─────────────────────┐
                         │     FDD User / UI   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │       FDD API       │
                         │ Generate / Query /   │
                         │ Human Review        │
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


        ┌──────────────────────────────────────────┐
        │                Data / AI Layer            │
        │                                          │
        │ Documents → PDF ingestion → Chunking     │
        │ → Embeddings → Vector Store → Retrieval  │
        │ → Evidence supplied to AI agents         │
        └──────────────────────────────────────────┘

3. Architectural Principles
3.1 Deterministic before probabilistic
Financial calculations such as revenue growth, EBITDA margin, working capital movements and customer concentration are performed using deterministic Python logic.
LLMs are used for reasoning, interpretation, synthesis and report generation.
This reduces the risk of allowing an LLM to perform calculations that require reproducibility and numerical accuracy.

3.2 Evidence before conclusions
AI agents do not receive unrestricted access to the underlying documents.
The retrieval layer identifies relevant evidence and supplies that evidence to the reasoning layer.
The intended flow is:

Question
   ↓
Retrieval
   ↓
Relevant evidence
   ↓
AI reasoning
   ↓
Structured finding
   ↓
Validation
   ↓
Evidence-backed answer

3.3 LLM proposes; application authorizes; code executes
The AI planner can propose which specialist capabilities are required.
The application does not blindly execute arbitrary AI-generated instructions.
Agent names are validated against an explicit allow-list and registry before execution.

LLM Planner
     ↓
Proposed agents
     ↓
Allow-list validation
     ↓
Agent registry
     ↓
Controlled execution

This provides a security boundary between probabilistic AI output and application execution.

3.4 Human judgement remains part of the workflow
FDD conclusions can influence investment decisions.
The platform therefore supports human review with three possible outcomes:
- Approved
- Amended
- Rejected
The system records the review status alongside the finding.

4. Core Components
FDD API
Provides the business-facing interface.
Current product operations:

POST /fdd/generate
POST /fdd/query
POST /fdd/review

The API hides the underlying specialist-agent implementation from the consuming UI.

FDD Orchestrator
Coordinates the end-to-end FDD workflow.
For full report generation it executes the required specialist analyses.
For question answering it invokes the planner, executes the selected specialist agents and optionally generates an executive summary.

AI Planner
The planner determines which specialist capabilities are relevant to a specific FDD question.
It is constrained by an explicit set of supported agents.
The planner does not have permission to execute arbitrary code or arbitrary tools.

Specialist Agents
The current specialist agents are:
- Revenue Agent
- EBITDA Agent
- Working Capital Agent
- Customer Concentration Agent
- Financial Anomaly Agent
Each agent has a focused responsibility and produces structured output.
This improves modularity, testability and explainability compared with a single general-purpose agent.

Retrieval Layer
The retrieval pipeline is:

PDF
 ↓
PDF Loader
 ↓
Text Chunks
 ↓
Embeddings
 ↓
Vector Store
 ↓
Semantic Search
 ↓
Evidence

Retrieved evidence contains source and page metadata to support provenance.

Validation Layer
The validation layer protects the boundary between AI output and application output.
Controls include:
- Pydantic schema validation
- deterministic financial calculations
- supported-agent allow-list
- evidence/source metadata
- confidence validation
- human review status
Report Synthesis
The report synthesis agent combines specialist findings into a structured FDD report.
The LLM is responsible for synthesis and narrative generation.
The application remains responsible for report structure and PDF generation.
5. Trust Boundaries
The major trust boundaries are:
External documents → ingestion
Documents are treated as untrusted input.
A document may contain malicious or misleading instructions and must not be treated as an authoritative system instruction.
Retrieval → LLM
Retrieved content is treated as evidence/data rather than instructions.
Planner → execution
Planner output is validated before any specialist agent is executed.
LLM output → application
AI-generated JSON is validated against application schemas before being accepted.
AI conclusion → human decision
High-impact findings can be reviewed and amended by a human before being treated as final.
6. Security Architecture
Primary threats considered:
- Prompt injection
- Malicious documents
- Unauthorized agent execution
- Unsupported AI output
- Incorrect financial calculations
- Irrelevant retrieval
- Data leakage
- API credential exposure
- Planner misrouting
Current controls include:
- Treating documents as untrusted data
- Explicit evidence-only prompting
- Agent allow-list
- Agent registry
- Structured Pydantic validation
- Deterministic financial calculations
- Source/page provenance
- Human review
- Environment-based API secrets
7. AI Responsibility Model
Capability	Technology	Responsibility
Financial calculations	Python	Deterministic computation
Document retrieval	Embeddings + vector store	Evidence retrieval
Financial reasoning	LLM	Interpretation
Agent selection	AI Planner	Capability selection
Agent authorization	Application	Security control
Report synthesis	LLM	Narrative synthesis
Output validation	Pydantic	Schema enforcement
Final judgement	Human	Accountability


8. Groundedness and Provenance
The platform distinguishes between:
Groundedness
Whether an AI-generated claim is supported by the evidence supplied to the model.
Accuracy
Whether the underlying financial information itself is correct.
The current architecture primarily controls groundedness through:
Retrieve
   ↓
Supply evidence
   ↓
Generate finding
   ↓
Capture source/page
   ↓
Validate structured output
   ↓
Human review

Deterministic calculations provide an additional control for numerical accuracy.
9. Failure Handling
The system should fail safely when an AI dependency is unavailable.
Examples:
- LLM unavailable → do not fabricate a finding.
- Retrieval unavailable → do not generate an unsupported conclusion.
- Invalid planner output → reject the plan.
- Unsupported agent → reject execution.
- Invalid structured output → reject the response.
- Human review rejected → finding must not be treated as approved.
Future production implementation can add:
- retries
- timeouts
- circuit breakers
- asynchronous execution
- model fallback
- observability and alerting
10. Scalability Considerations
The current implementation is a prototype architecture.
For production scale:
API
 ↓
Queue
 ↓
Worker Pool
 ↓
Independent Specialist Agents
 ↓
Result Store
 ↓
Report Synthesis

The API layer should remain stateless.
Specialist agents can scale independently.
Long-running FDD generation should be asynchronous rather than blocking an HTTP request.
Tenant isolation, authentication, authorization, rate limiting, cost controls and centralized observability would be added for enterprise deployment.
11. Architectural Trade-offs
Multi-agent vs single-agent
Multi-agent architecture introduces additional orchestration complexity but provides:
- clearer responsibilities
- independent testing
- controlled execution
- easier extension
- better explainability
A single agent would be simpler but would concentrate multiple responsibilities into one probabilistic component.
RAG vs fine-tuning
RAG is preferred for deal-specific FDD information because the underlying documents change from transaction to transaction and evidence provenance is important.
Fine-tuning would be more appropriate for changing model behaviour or specialised response patterns rather than supplying current deal information.
LLM vs deterministic logic
LLMs are valuable for interpretation and synthesis but should not be the source of truth for financial calculations.
12. Current vs Production Architecture
Current prototype
- FastAPI
- Python specialist agents
- OpenAI models
- Chroma vector store
- Pydantic validation
- Local PDF generation
- Synthetic financial data
- Human review workflow
- Evaluation suite
Production evolution
- Enterprise identity and RBAC
- Secure document storage
- Managed vector database
- Asynchronous orchestration
- Model gateway/router
- Observability
- Audit logging
- Secrets management
- Tenant isolation
- Cost controls
- Resilience and disaster recovery
- Enterprise deployment on cloud infrastructure
13. Key Architectural Principle
The platform deliberately separates four types of work:
Deterministic computation
        +
Evidence retrieval
        +
Probabilistic reasoning
        +
Human judgement

The architecture does not attempt to make the LLM responsible for every decision.
This separation provides a foundation for building an enterprise-grade AI financial due diligence platform while maintaining control, explainability and auditability.

