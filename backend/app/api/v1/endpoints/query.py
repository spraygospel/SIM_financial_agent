# backend/app/api/v1/endpoints/query.py
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from backend.app.services.agent_service import agent_service, conversation_memory

router = APIRouter()

class QueryRequest(BaseModel):
    user_query: str
    session_id: str

# Definisikan model yang lebih detail untuk respons JSON kita
class ExecutiveSummaryItem(BaseModel):
    value: Union[str, int, float]
    label: str

class DataTableHeader(BaseModel):
    accessorKey: str
    header: str

class StructuredResponse(BaseModel):
    # Field ini bisa ada atau tidak. Jika tidak ada, defaultnya adalah list kosong.
    executive_summary: Optional[List[ExecutiveSummaryItem]] = Field(default_factory=list)
    
    # Field ini sekarang juga opsional, untuk menangani kasus error total.
    final_narrative: Optional[str] = "Tidak ada narasi yang dihasilkan."
    
    data_quality_score: Optional[int] = None
    warnings_for_display: Optional[List[str]] = Field(default_factory=list)
    
    # Field tabel juga dibuat opsional
    data_table_headers: Optional[List[DataTableHeader]] = Field(default_factory=list)
    data_table_for_display: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

# Model respons utama sekarang mengharapkan objek StructuredResponse
class QueryResponse(BaseModel):
    response: StructuredResponse

@router.post("/query", response_model=QueryResponse)
async def process_user_query(request: QueryRequest):
    try:
        # Panggilan ini sekarang akan berhasil
        result = await agent_service.process_query(
            user_query=request.user_query,
            session_id=request.session_id,
        )
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/session/start")
async def start_session():
    session_id = str(uuid.uuid4())
    conversation_memory[session_id] = []
    
    return {
        "session_id": session_id,
        "greeting_message": "Selamat datang di AI Financial Analyst! Apa yang bisa saya bantu analisis hari ini?",
        "suggested_queries": [
          "Tampilkan 5 customer yang piutangnya belum lunas",
          "Berapa total piutang dari semua customer?"
        ]
    }