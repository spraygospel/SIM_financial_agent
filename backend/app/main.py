# backend/app/main.py
from fastapi import FastAPI
import sys 
import os 
from dotenv import load_dotenv 
from pathlib import Path 

# Tentukan path ke .env di direktori backend/
# app_dir akan menjadi .../backend/app
app_dir = Path(__file__).resolve().parent 
# backend_dir akan menjadi .../backend
backend_dir = app_dir.parent 
dotenv_path_in_main = backend_dir / '.env'

if dotenv_path_in_main.exists():
    print(f"[main.py] Loading .env from: {dotenv_path_in_main}", file=sys.stderr)
    load_dotenv(dotenv_path=dotenv_path_in_main)
else:
    print(f"[main.py] .env file not found at {dotenv_path_in_main}. Relying on global env vars or config.py's loading.", file=sys.stderr)
    # Jika config.py juga tidak menemukannya, settings.LLM_API_KEY akan None.

# Import harus setelah potensi load_dotenv agar settings terisi dengan benar
from backend.app.api.v1.endpoints import query as query_router_v1 
from backend.app.core.config import settings 

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

app.include_router(query_router_v1.router, prefix="/api/v1/query", tags=["Query Processing V1"])

@app.get("/", tags=["Root"])
async def read_root():
    print("--- Root endpoint / called ---", file=sys.stderr) 
    return {"message": f"Welcome to {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}. LLM Key Loaded: {'Yes' if settings.LLM_API_KEY else 'No'}"}

# Untuk menjalankan via "python backend/app/main.py" (development only):
# if __name__ == "__main__":
#     import uvicorn
#     print(f"Starting Uvicorn server for {settings.PROJECT_NAME} directly from main.py...", file=sys.stderr)
#     # Jalankan Uvicorn dengan menargetkan objek 'app' dalam modul 'main' di dalam package 'backend.app'
#     # Ini mengasumsikan Anda menjalankan skrip ini dari root proyek (ai_agent_project_root)
#     # atau PYTHONPATH sudah mencakup root proyek.
#     # Cara paling umum dan direkomendasikan adalah:
#     # uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
#     # Jika Anda menjalankan python backend/app/main.py, maka uvicorn perlu tahu letak 'app'
#     # Cara sederhana: uvicorn.run("main:app", ...) jika main.py adalah entry point langsung.
#     # Menggunakan string "backend.app.main:app" lebih robust jika direktori kerja bervariasi.
#
#     # Jika menjalankan `python backend/app/main.py` dari `ai_agent_project_root/`
#     # dan `backend` adalah package:
#     # uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
#     # Jika menjalankan dari `ai_agent_project_root/backend/app/`:
#     # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
#
#     # Cara yang lebih baik adalah menjalankan uvicorn dari command line:
#     # cd ai_agent_project_root
#     # uvicorn backend.app.main:app --reload --port 8000