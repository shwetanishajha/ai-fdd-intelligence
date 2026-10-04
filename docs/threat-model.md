# AI-FDD Intelligence — Threat Model

## 1. System Scope

AI-FDD Intelligence is an agentic AI platform for financial due diligence.

The system combines:

- Document ingestion
- Document chunking
- Embedding generation
- Vector retrieval
- Specialist FDD agents
- AI-based task planning
- Controlled agent execution
- Executive summarisation
- Structured output validation
- Human review

All demonstration data is synthetic.

---

## 2. Security Objectives

The platform must protect:

1. Confidential financial information
2. Integrity of financial findings
3. Integrity of retrieved evidence
4. Agent execution boundaries
5. LLM interaction boundaries
6. API credentials and secrets
7. Auditability and provenance

---

## 3. Trust Boundaries

### Boundary 1 — External Documents → Ingestion

Documents are treated as untrusted input.

Potential threats:

- Malicious instructions embedded in documents
- Prompt injection
- Malicious or malformed files
- Unexpected document content

Control:

- Treat document content as data, not instructions.

---

### Boundary 2 — Retrieval → LLM

Retrieved content is supplied to the LLM as evidence.

Potential threat:

- Retrieved text attempts to override system instructions.

Control:

- Explicitly instruct the model that retrieved content is untrusted evidence.
- Never allow retrieved content to redefine system behaviour.

---

### Boundary 3 — LLM Planner → Agent Execution

The planner proposes which agents should execute.

Potential threat:

- The LLM proposes an unauthorized agent.

Control:

- Explicit agent allow-list.
- Pydantic validation.
- Deterministic agent registry.
- Unsupported agents are rejected.

---

### Boundary 4 — Agent → Financial Data

Specialist agents access financial datasets.

Potential threats:

- Incorrect calculations
- Data manipulation
- Unsupported conclusions

Controls:

- Deterministic financial calculations.
- Evidence-backed findings.
- Structured outputs.
- Automated tests.

---

### Boundary 5 — LLM Output → Application

LLM-generated output is consumed by application code.

Potential threats:

- Invalid structure
- Unexpected values
- Unsupported risk classifications

Controls:

- Pydantic schema validation.
- Explicit allowed values.
- Validation before application use.

---

## 4. Key Threats

| Threat | Impact | Primary Control |
|---|---|---|
| Prompt injection | High | Treat retrieved content as untrusted |
| Unauthorized agent execution | High | Agent allow-list + registry |
| Incorrect financial calculation | High | Deterministic calculations |
| Unsupported LLM output | Medium | Pydantic validation |
| Data leakage | High | Synthetic data + secret management |
| Malicious documents | High | Input validation |
| Retrieval of irrelevant evidence | Medium | Retrieval evaluation |
| Planner misrouting | Medium | Planner evaluation |
| API credential exposure | High | Environment-based secrets |

---

## 5. Agent Execution Principle

The LLM planner is never granted arbitrary code execution.

The execution model is:

LLM Planner
→ Structured Plan
→ Validation
→ Allow-listed Agent
→ Deterministic Python Function

This creates a deterministic security boundary around agent execution.

---

## 6. Security Testing Strategy

The platform should test:

- Prompt injection resistance
- Unsupported agent rejection
- Invalid structured output rejection
- Retrieval relevance
- Calculation correctness
- Planner decision accuracy
- Evidence grounding
- Secret handling

---

## 7. Residual Risks

The following risks remain for future implementation:

- Prompt injection within retrieved documents
- LLM hallucination
- Incorrect interpretation of evidence
- Data poisoning
- Model/API availability
- Insufficient authentication and authorisation
- Incomplete audit logging
- Sensitive-data exposure in production deployments

These risks require additional controls before production deployment.