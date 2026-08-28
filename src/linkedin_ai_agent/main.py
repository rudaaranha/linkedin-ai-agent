from fastapi import FastAPI

app = FastAPI(
    title="Linkedin AI Agent",
    description="AI-powered Linkedin content automation pipeline",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "linkedin-ai-agent",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
