# backend/app/services/session_manager.py
from typing import Dict, Optional, Any
import asyncio
from datetime import datetime, timedelta
import uuid

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, asyncio.Queue] = {}
        self.session_timestamps: Dict[str, datetime] = {}
        self.cleanup_interval_seconds = 300  # 5 menit
        self.session_timeout_seconds = 600   # 10 menit
        
    async def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = asyncio.Queue()
        self.session_timestamps[session_id] = datetime.now()
        print(f"Sesi baru dibuat: {session_id}")
        return session_id
    
    async def get_queue(self, session_id: str) -> Optional[asyncio.Queue]:
        return self.sessions.get(session_id)

    async def send_to_queue(self, session_id: str, data: Dict[str, Any]):
        queue = self.sessions.get(session_id)
        if queue:
            await queue.put(data)
    
    async def cleanup_old_sessions(self):
        while True:
            await asyncio.sleep(self.cleanup_interval_seconds)
            now = datetime.now()
            expired_sessions = [
                sid for sid, ts in self.session_timestamps.items() 
                if now - ts > timedelta(seconds=self.session_timeout_seconds)
            ]
            for sid in expired_sessions:
                if sid in self.sessions:
                    del self.sessions[sid]
                if sid in self.session_timestamps:
                    del self.session_timestamps[sid]
                print(f"Sesi kadaluarsa dibersihkan: {sid}")

session_manager = SessionManager()