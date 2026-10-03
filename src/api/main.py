from fastapi import FastAPI

app = FastAPI(
    title="AI-FDD Intelligence",
    description="Evidence-backed AI platform for financial due diligence",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}