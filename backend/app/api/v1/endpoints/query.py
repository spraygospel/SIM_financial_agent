# backend/app/api/v1/endpoints/query.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

from backend.app.services.agent_service import agent_service

router = APIRouter()

class QueryRequest(BaseModel):
    user_query: str
    session_id: str

class QueryResponse(BaseModel):
    response: str

@router.post("/query", response_model=QueryResponse)
async def process_user_query(request: QueryRequest):
    try:
        # Panggil service yang sudah diperbaiki
        result = await agent_service.process_query(
            user_query=request.user_query,
            session_id=request.session_id,
        )
        
        # Service sekarang mengembalikan dict yang formatnya sudah benar
        return result
    except Exception as e:
        # Menambahkan penanganan error yang lebih baik
        print(f"ERROR in process_user_query: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/session/start")
async def start_session():
    import uuid
    # Bersihkan memori sesi lama jika ada (opsional, tapi praktik yang baik)
    from backend.app.services.agent_service import conversation_memory
    session_id = str(uuid.uuid4())
    conversation_memory[session_id] = []
    
    return {"session_id": session_id}