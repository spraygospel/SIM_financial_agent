# backend/app/main.py
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints import query
from backend.app.core.session_manager import session_manager

app = FastAPI(title="AI Agent Backend")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(session_manager.cleanup_old_sessions())

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/api/v1", tags=["Query Processing"])

@app.get("/")
def read_root():
    return {"message": "AI Agent Backend is running"}