# scripts/test_advanced_scenario.py

import requests
import json
import time
from pprint import pprint

BASE_URL = "http://localhost:8000/api/v1"

def print_step(n, text):
    print(f"\n🔄 Langkah {n}: {text}")

def print_query(query):
    print(f"   -> Mengirim query: '{query}'")

def print_response(response_json):
    print("   <- Respons diterima:")
    # Cetak respons dengan rapi
    response_text = response_json.get("response", "Kunci 'response' tidak ditemukan.")
    print("      " + "\n      ".join(response_text.splitlines()))


def run_advanced_test():
    """
    Menjalankan tes end-to-end dengan skenario yang lebih kompleks dan berlapis
    untuk menguji kemampuan analitis dan kontekstual agent.
    """
    print("--- Memulai Tes Skenario Lanjutan ---")
    
    session_id = None
    
    try:
        # Langkah 1: Memulai sesi
        print_step(1, "Memulai sesi baru...")
        start_response = requests.get(f"{BASE_URL}/session/start")
        start_response.raise_for_status()
        session_id = start_response.json()["session_id"]
        print(f"   ✅ Sesi berhasil dimulai. ID: {session_id}")

        # Langkah 2: Query kompleks yang membutuhkan JOIN
        # "Tampilkan 5 nama customer yang piutangnya belum lunas beserta nilai piutangnya"
        query1 = "Tampilkan 5 nama customer yang piutangnya belum lunas beserta sisa tagihannya. Urutkan dari yang paling besar."
        print_step(2, "Mengirim query kompleks (JOIN & Sisa Tagihan)...")
        print_query(query1)
        response1 = requests.post(f"{BASE_URL}/query", json={"user_query": query1, "session_id": session_id}, timeout=120)
        response1.raise_for_status()
        print_response(response1.json())

        # Langkah 3: Query modifikasi (FILTER) terhadap hasil sebelumnya
        query2 = "Oke, dari daftar itu, coba filter untuk PT Sinar Harapan saja."
        print_step(3, "Mengirim query modifikasi (FILTER)...")
        print_query(query2)
        response2 = requests.post(f"{BASE_URL}/query", json={"user_query": query2, "session_id": session_id}, timeout=120)
        response2.raise_for_status()
        print_response(response2.json())

        # Langkah 4: Query analitis yang membutuhkan perhitungan
        query3 = "Berapa total piutang dari semua customer yang belum lunas?"
        print_step(4, "Mengirim query analitis (SUM)...")
        print_query(query3)
        response3 = requests.post(f"{BASE_URL}/query", json={"user_query": query3, "session_id": session_id}, timeout=120)
        response3.raise_for_status()
        print_response(response3.json())

        # Langkah 5: Interaksi sosial
        query4 = "Luar biasa, terima kasih banyak atas bantuannya!"
        print_step(5, "Mengirim interaksi sosial...")
        print_query(query4)
        response4 = requests.post(f"{BASE_URL}/query", json={"user_query": query4, "session_id": session_id}, timeout=60)
        response4.raise_for_status()
        print_response(response4.json())

        print("\n\n🎉 Tes Skenario Lanjutan BERHASIL! 🎉")

    except requests.Timeout:
        print("🔥 GAGAL: Permintaan timeout. Proses agent mungkin terlalu lama.")
    except requests.RequestException as e:
        print(f"🔥 GAGAL saat menjalankan tes. Error: {e}")
        if 'response1' in locals() and response1: print("Respons Terakhir:", response1.text)
        elif 'response2' in locals() and response2: print("Respons Terakhir:", response2.text)
        # dst.

if __name__ == "__main__":
    run_advanced_test()