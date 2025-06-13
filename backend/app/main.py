# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints import query

# Tidak ada lagi load_dotenv atau check_env_vars di sini.
# Semua itu sudah ditangani secara otomatis saat 'query' diimpor,
# yang pada gilirannya mengimpor 'agent_service', lalu 'config'.

app = FastAPI(title="AI Agent Backend")

# Definisikan origin yang diizinkan
origins = [
    "http://localhost:5173",  # Alamat default untuk Vite
    "http://localhost:3000",  # Alamat default untuk Create React App
]

# Tambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sertakan router dari endpoint
app.include_router(query.router, prefix="/api/v1", tags=["Query Processing"])

# Endpoint root untuk pengecekan status
@app.get("/")
def read_root():
    return {"message": "AI Agent Backend is running"}