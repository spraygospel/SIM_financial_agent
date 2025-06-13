# scripts/test_backend_flow.py
import requests
import json
import os
from dotenv import load_dotenv

# Muat environment variables dari root .env file
# Skrip ini mengasumsikan ia dijalankan dari root direktori proyek,
# atau .env file ada di path yang bisa dijangkau.
# Sesuaikan path jika perlu.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Konfigurasi dari environment variables
# Pastikan Anda sudah menjalankan backend di alamat ini
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def print_section_header(title):
    """Mencetak header untuk setiap bagian output agar mudah dibaca."""
    print("\n" + "="*80)
    print(f" {title.upper()} ".center(80, "="))
    print("="*80)

def print_pretty_json(data, indent=2):
    """Mencetak JSON dengan format yang rapi."""
    print(json.dumps(data, indent=indent, ensure_ascii=False))

def run_test():
    """Menjalankan alur pengujian lengkap."""
    session = requests.Session()
    session_id = None

    try:
        # --- LANGKAH 1: MEMULAI SESI BARU ---
        print_section_header("1. Memulai Sesi Baru")
        start_session_url = f"{BACKEND_URL}/api/v1/session/start"
        print(f"[*] Mengirim GET request ke: {start_session_url}")
        
        response = session.get(start_session_url, timeout=10)
        response.raise_for_status()  # Akan error jika status code bukan 2xx
        
        session_data = response.json()
        session_id = session_data.get("session_id")
        
        if not session_id:
            raise ValueError("Gagal mendapatkan session_id dari server.")
            
        print(f"[+] SUKSES! Session ID diterima: {session_id}")

        # --- LANGKAH 2: MENGIRIM QUERY PENGGUNA ---
        print_section_header("2. Mengirim Query untuk Laporan Piutang")
        query_url = f"{BACKEND_URL}/api/v1/query"
        user_query = "Tunjukkan customer siapa saja yang belum lunas membayar beserta due date nya"
        
        payload = {
            "user_query": user_query,
            "session_id": session_id
        }
        
        print(f"[*] Mengirim POST request ke: {query_url}")
        print("[*] Payload:")
        print_pretty_json(payload)
        
        # Timeout bisa diperpanjang karena proses agent bisa memakan waktu
        response = session.post(query_url, json=payload, timeout=120) 
        response.raise_for_status()
        
        report_data = response.json()
        
        print("[+] SUKSES! Respons terstruktur diterima dari backend.")

        # --- LANGKAH 3: MEMVALIDASI DAN MENCETAK RESPONS ---
        print_section_header("3. Menganalisis Respons Terstruktur")
        
        # Validasi kunci-kunci utama yang dibutuhkan oleh UI
        required_keys = [
            "executive_summary",
            "final_narrative",
            "data_table_for_display",
            "warnings_for_display",
            "quality_score"
        ]
        
        print("[*] Memeriksa keberadaan kunci-kunci yang dibutuhkan UI...")
        missing_keys = [key for key in required_keys if key not in report_data]
        
        if missing_keys:
            print(f"\n[!] GAGAL: Kunci berikut tidak ditemukan dalam respons: {missing_keys}")
            print("\nRespons mentah yang diterima:")
            print_pretty_json(report_data)
            return

        print("[+] Semua kunci yang dibutuhkan oleh UI ditemukan!")
        
        # Mencetak setiap bagian dari laporan
        print("\n--- Ringkasan Eksekutif ---")
        print_pretty_json(report_data["executive_summary"])

        print("\n--- Analisis Naratif ---")
        print(report_data["final_narrative"])

        print("\n--- Tabel Data (Contoh 3 baris pertama) ---")
        print_pretty_json(report_data["data_table_for_display"][:3])

        print("\n--- Catatan Kualitas & Peringatan ---")
        print_pretty_json(report_data["warnings_for_display"])

        print(f"\n--- Skor Kualitas ---")
        print(f"Skor: {report_data['quality_score']}/100")
        
        print_section_header("Pengujian Selesai dengan SUKSES")

    except requests.exceptions.RequestException as e:
        print(f"\n[!!!] GAGAL: Terjadi kesalahan koneksi ke backend: {e}")
        print("[!!!] Pastikan backend Anda sedang berjalan di alamat yang benar.")
    except Exception as e:
        print(f"\n[!!!] GAGAL: Terjadi kesalahan tak terduga: {e}")

if __name__ == "__main__":
    run_test()