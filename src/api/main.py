from fastapi import FastAPI

from src.agents.fdd_analyzer import analyze_fdd_question
from src.agents.agentic_fdd import run_agentic_fdd


app = FastAPI(
    title="AI-FDD Intelligence",
    description="Evidence-backed AI platform for financial due diligence",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/fdd/analyze")
def analyze(question: str):
    return analyze_fdd_question(question)


@app.get("/fdd/agentic")
def agentic_analyze(question: str):
    return run_agentic_fdd(question)