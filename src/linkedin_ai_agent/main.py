from fastapi import FastAPI

from linkedin_ai_agent.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="AI-powered Linkedin content automation pipeline",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": settings.app_name,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
