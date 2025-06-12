# scripts/test_e2e_phase3.py (Versi Tool Calling)

import requests
import json
import time
from pprint import pprint

BASE_URL = "http://localhost:8000/api/v1"

def run_e2e_test():
    """Menjalankan tes end-to-end untuk arsitektur tool calling."""
    print("--- Memulai Tes End-to-End untuk Agent Tool Calling ---")

    # 1. Mulai sesi baru
    print("\n🔄 Langkah 1: Memulai sesi baru...")
    try:
        start_response = requests.get(f"{BASE_URL}/session/start")
        start_response.raise_for_status()
        session_id = start_response.json()["session_id"]
        print(f"✅ Sesi berhasil dimulai. ID: {session_id}")
    except requests.RequestException as e:
        print(f"🔥 GAGAL memulai sesi. Pastikan server FastAPI utama berjalan. Error: {e}")
        return

    # 2. Kirim query yang membutuhkan tool
    print("\n🔄 Langkah 2: Mengirim query yang akan memanggil tool database...")
    query1 = "tampilkan 2 customer pertama dari tabel mastercustomer"
    query_payload1 = { "user_query": query1, "session_id": session_id }
    
    try:
        print(f"Mengirim query: '{query1}'")
        query_response = requests.post(f"{BASE_URL}/query", json=query_payload1, timeout=90)
        query_response.raise_for_status()
        result1 = query_response.json()

        print("✅ Respons pertama berhasil diterima.")
        pprint(result1)

        # 3. Kirim query lanjutan dalam sesi yang sama
        print("\n🔄 Langkah 3: Mengirim query lanjutan...")
        query2 = "Bagus, terima kasih!"
        query_payload2 = { "user_query": query2, "session_id": session_id }
        
        print(f"Mengirim query: '{query2}'")
        query_response2 = requests.post(f"{BASE_URL}/query", json=query_payload2, timeout=90)
        query_response2.raise_for_status()
        result2 = query_response2.json()

        print("✅ Respons kedua berhasil diterima.")
        pprint(result2)

        print("\n🎉 Tes End-to-End BERHASIL! 🎉")

    except requests.Timeout:
        print("🔥 GAGAL: Permintaan timeout. Proses LLM atau database mungkin terlalu lama.")
    except requests.RequestException as e:
        print(f"🔥 GAGAL saat mengirim query. Error: {e}")
        if 'response' in locals() or 'query_response' in locals():
            print("Detail Respons Error:", query_response.text if 'query_response' in locals() else 'N/A')

if __name__ == "__main__":
    run_e2e_test()