# backend/app/core/session_manager.py
from typing import Dict, Optional, Any
import asyncio
from datetime import datetime, timedelta
import uuid
import json

class SessionManager:
    def __init__(self):
        # Kunci: session_id, Nilai: asyncio.Queue
        self.sessions: Dict[str, asyncio.Queue] = {}
        self.session_timestamps: Dict[str, datetime] = {}
        # Kita buat timeout lebih pendek untuk development
        self.session_timeout_seconds = 600  # 10 menit

    async def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        queue = asyncio.Queue()
        self.sessions[session_id] = queue
        self.session_timestamps[session_id] = datetime.now()
        print(f"--- Sesi baru dibuat: {session_id} ---")
        return session_id

    async def get_queue(self, session_id: str) -> Optional[asyncio.Queue]:
        return self.sessions.get(session_id)
    
    async def send_event(self, session_id: str, event_type: str, data: Dict[str, Any]):
        queue = self.sessions.get(session_id)
        if queue:
            event_data = json.dumps({"event_type": event_type, "data": data})
            await queue.put(event_data)

    async def close_session(self, session_id: str):
        if session_id in self.sessions:
            queue = self.sessions[session_id]
            # Kirim sinyal berhenti ke queue
            await queue.put(None) 
            del self.sessions[session_id]
            del self.session_timestamps[session_id]
            print(f"--- Sesi ditutup: {session_id} ---")

    async def cleanup_old_sessions_task(self):
        """Tugas latar belakang untuk membersihkan sesi lama."""
        while True:
            await asyncio.sleep(300) # Cek setiap 5 menit
            now = datetime.now()
            old_sessions = [
                sid for sid, ts in self.session_timestamps.items()
                if now - ts > timedelta(seconds=self.session_timeout_seconds)
            ]
            for sid in old_sessions:
                print(f"--- Membersihkan sesi lama karena timeout: {sid} ---")
                await self.close_session(sid)

# Buat satu instance global untuk digunakan di seluruh aplikasi
session_manager = SessionManager()