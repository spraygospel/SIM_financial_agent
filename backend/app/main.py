# backend/app/main.py

from fastapi import FastAPI
from backend.app.api.v1.endpoints import query

app = FastAPI(title="AI Agent Backend")

app.include_router(query.router, prefix="/api/v1", tags=["Query Processing"])

@app.get("/")
def read_root():
    return {"message": "AI Agent Backend is running"}