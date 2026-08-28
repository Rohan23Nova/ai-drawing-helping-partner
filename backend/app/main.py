from fastapi import FastAPI


app = FastAPI(
    title="AI Drawing Helping Partner",
    description="An AI-powered drawing assistance API.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "AI Drawing Helping Partner API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }