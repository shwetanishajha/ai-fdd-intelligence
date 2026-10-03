from fastapi import FastAPI
from src.agents.fdd_analyzer import analyze_fdd_question

app = FastAPI(
    title="AI-FDD Intelligence",
    description="Evidence-backed AI platform for financial due diligence",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}

    from src.agents.fdd_analyzer import analyze_fdd_question


@app.get("/fdd/analyze")
def analyze(question: str):
    return analyze_fdd_question(question)