# scripts/run_dev_servers.py (Versi HTTP)

import subprocess, time, sys
import time
import sys
from pathlib import Path

# --- Setup Path (Penting agar bisa impor config) ---
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from backend.app.core.config import settings


servers = {
    "mysql_server": {
        "module": "backend.mcp_servers.mysql_server.main:app",
        "url": settings.MYSQL_MCP_SERVER_URL,
    },
    "graphiti_server": {
        "module": "backend.mcp_servers.graphiti_server.main:app",
        "url": settings.GRAPHITI_MCP_SERVER_URL,
    }
}

processes = []

def get_port_from_url(url: str) -> int:
    try:
        return int(url.split(":")[-1])
    except (ValueError, IndexError):
        raise ValueError(f"URL tidak valid atau tidak mengandung port: {url}")

try:
    print("--- Memulai semua server MCP sebagai layanan HTTP ---")
    for name, config in servers.items():
        try:
            port = get_port_from_url(config["url"])
            
            command = [
                sys.executable, "-m", "uvicorn",
                config["module"],
                "--host", "0.0.0.0",
                "--port", str(port),
            ]
            
            print(f"🚀 Menjalankan {name} di port {port}...")
            process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
            processes.append(process)
            print(f"✅ Server '{name}' berjalan dengan PID: {process.pid}")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Gagal menjalankan server '{name}': {e}")

    if not processes:
        print("🔥 Tidak ada server yang berhasil dijalankan. Keluar.")
        sys.exit(1)

    print("\n✅ Semua server telah dijalankan. Tekan Ctrl+C di jendela ini untuk menghentikan semua.")
    
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n--- Menerima sinyal interupsi (Ctrl+C). Menghentikan semua server... ---")

finally:
    for process in processes:
        print(f"Terminating PID: {process.pid}...")
        process.terminate()
    print("--- Semua server telah dihentikan. ---")