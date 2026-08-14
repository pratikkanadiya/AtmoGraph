from fastapi import FastAPI
from app.database.neo4j import verify_connection

app = FastAPI(
    title="AtmoGraph API",
    description="Supply Chain Ripple Effect Predictor",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "AtmoGraph",
        "status": "running"
    }


@app.get("/health")
def health():
    try:
        message = verify_connection()

        return {
            "status": "healthy",
            "database": "Neo4j",
            "connection": message
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "Neo4j",
            "error": str(e)
        }