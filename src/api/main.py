from fastapi import FastAPI
from pydantic import BaseModel

from src.agents.fdd_analyzer import analyze_fdd_question
from src.agents.agentic_fdd import run_agentic_fdd
from src.validation.human_review import review_finding
from src.agents.fdd_product import run_fdd


app = FastAPI(
    title="AI-FDD Intelligence",
    description="Evidence-backed AI platform for financial due diligence",
    version="0.1.0",
)


class ReviewRequest(BaseModel):
    finding: dict
    decision: str
    amended_finding: str | None = None


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/fdd/analyze")
def analyze(question: str):
    return analyze_fdd_question(question)


@app.get("/fdd/agentic")
def agentic_analyze(question: str):
    return run_agentic_fdd(question)

@app.post("/fdd/generate")
def generate_fdd():
    return run_fdd(mode="generate")


@app.post("/fdd/query")
def query_fdd(question: str):
    return run_fdd(mode="query", question=question)


@app.post("/fdd/review")
def review(request: ReviewRequest):
    return review_finding(
        finding=request.finding,
        decision=request.decision,
        amended_finding=request.amended_finding,
    )