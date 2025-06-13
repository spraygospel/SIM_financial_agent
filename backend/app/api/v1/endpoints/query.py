# backend/app/api/v1/endpoints/query.py
import asyncio
import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict

from backend.app.core.session_manager import session_manager
from backend.app.services.agent_service import agent_service

router = APIRouter()

class QueryRequest(BaseModel):
    user_query: str
    session_id: str

@router.post("/create_session")
async def create_session():
    session_id = await session_manager.create_session()
    return {"session_id": session_id, "greeting_message": "Selamat datang!"}

@router.post("/query")
async def submit_query(request: QueryRequest):
    queue = await session_manager.get_queue(request.session_id)
    if not queue:
        raise HTTPException(status_code=404, detail="Sesi tidak valid.")
    
    # Hanya taruh pesan query di queue
    await queue.put({"type": "USER_QUERY", "content": request.user_query})
    return {"status": "diterima"}

@router.get("/stream_updates/{session_id}")
async def stream_updates(session_id: str, request: Request):
    queue = await session_manager.get_queue(session_id)
    if not queue:
        raise HTTPException(status_code=404, detail="Sesi tidak ditemukan.")
        
    async def event_generator():
        # Langkah 1: Tunggu pesan query pertama dari pengguna
        user_query_event = await queue.get()
        if user_query_event.get("type") != "USER_QUERY":
            # Jika pesan pertama bukan query, tutup koneksi
            return
        
        # Langkah 2: Setelah query diterima, jalankan proses agent
        # Proses agent sekarang berjalan di dalam generator ini, bukan di background task
        await agent_service.process_query_and_stream_updates(
            session_id=session_id,
            user_query=user_query_event["content"]
        )

        # Langkah 3: Kirim sisa pesan dari queue (jika ada)
        while not queue.empty():
            if await request.is_disconnected():
                break
            message = await queue.get()
            yield f"data: {json.dumps(message)}\n\n"
            if message.get("event_type") == "STREAM_END":
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")