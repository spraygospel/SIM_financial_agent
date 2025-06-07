import mysql.connector
from mysql.connector import errorcode
import json
import os
from dotenv import load_dotenv

# --- Konfigurasi ---
# Muat variabel lingkungan dari file .env di direktori backend
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

MYSQL_CONFIG = {
    'host': os.getenv("MYSQL_HOST", "localhost"),
    'user': os.getenv("MYSQL_USER", "root"),
    'password': os.getenv("MYSQL_PASSWORD"),
    'database': os.getenv("MYSQL_DATABASE", "sim_testgeluran") # Pastikan ini nama DB yang benar
}

# Path ke file JSON yang berisi draf metadata Graphiti
# Asumsi file ini ada di data_samples/ dan berisi gabungan semua bagian yang sudah kita buat
JSON_MAPPING_FILE = os.path.join(os.path.dirname(__file__), '..', 'data_samples', 'graphiti_semantic_mapping.json')

# Daftar tabel yang memang sengaja ingin diabaikan dan tidak perlu ada di JSON mapping
# Sesuaikan jika ada tabel sistem atau tabel yang tidak relevan untuk AI Agent
TABLES_TO_IGNORE_IN_VERIFICATION = [
    # 'phinxlog', 
    # 'users_system_internal', 
]

def get_tables_from_mysql(connection):
    """
    Mengambil daftar semua nama tabel dari database MySQL.
    """
    tables = []
    cursor = connection.cursor()
    db_name = MYSQL_CONFIG['database']
    
    cursor.execute("SHOW TABLES;")
    tables_data = cursor.fetchall()
    for row_tuple in tables_data:
        table_name = row_tuple[0] # Nama tabel ada di elemen pertama tuple
        if table_name not in TABLES_TO_IGNORE_IN_VERIFICATION:
            tables.append(table_name)
            
    cursor.close()
    return tables

def get_tables_from_json(json_filepath):
    """
    Membaca file JSON dan mengembalikan daftar nama tabel yang didefinisikan.
    """
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Asumsi file JSON adalah dictionary di mana setiap key adalah nama tabel
        return list(data.keys())
    except FileNotFoundError:
        print(f"Error: File JSON '{json_filepath}' tidak ditemukan.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File JSON '{json_filepath}' bukan format JSON yang valid.")
        return None
    except Exception as e:
        print(f"Error saat membaca file JSON: {e}")
        return None

def main():
    if not MYSQL_CONFIG.get('password') or not MYSQL_CONFIG.get('database'):
        print("Error: Pastikan MYSQL_PASSWORD dan MYSQL_DATABASE sudah diatur di file .env pada direktori 'backend/'.")
        return

    # 1. Baca tabel dari file JSON
    print(f"Membaca definisi tabel dari file: {JSON_MAPPING_FILE}")
    tables_in_json = get_tables_from_json(JSON_MAPPING_FILE)
    if tables_in_json is None:
        return # Berhenti jika ada error saat baca JSON

    num_tables_in_json = len(tables_in_json)
    print(f"Jumlah tabel yang didefinisikan di file JSON: {num_tables_in_json}")
    # print("Daftar tabel di JSON:", sorted(tables_in_json)) # Uncomment untuk melihat daftarnya

    # 2. Koneksi ke MySQL dan ambil daftar tabel
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        print(f"\nBerhasil terkoneksi ke MySQL database: {MYSQL_CONFIG['database']}")
        
        tables_in_mysql_db = get_tables_from_mysql(connection)
        connection.close()
        
        num_tables_in_mysql = len(tables_in_mysql_db)
        print(f"Jumlah tabel aktual di database MySQL (setelah filter ignore): {num_tables_in_mysql}")
        # print("Daftar tabel di MySQL:", sorted(tables_in_mysql_db)) # Uncomment untuk melihat daftarnya

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Username atau password MySQL salah.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Error: Database '{MYSQL_CONFIG['database']}' tidak ditemukan.")
        else:
            print(f"Error MySQL lainnya: {err}")
        return
    except Exception as e:
        print(f"Terjadi error yang tidak terduga saat koneksi ke MySQL: {e}")
        return

    # 3. Bandingkan dan temukan tabel yang belum didefinisikan di JSON
    print("\n--- Verifikasi Cakupan Tabel ---")
    
    set_tables_in_json = set(tables_in_json)
    set_tables_in_mysql = set(tables_in_mysql_db)

    tables_defined_in_json_but_not_in_db = sorted(list(set_tables_in_json - set_tables_in_mysql))
    tables_in_db_but_not_in_json = sorted(list(set_tables_in_mysql - set_tables_in_json))

    if not tables_defined_in_json_but_not_in_db and not tables_in_db_but_not_in_json:
        print("Sinkron! Semua tabel di database MySQL telah didefinisikan di file JSON (setelah filter ignore).")
    else:
        if tables_in_db_but_not_in_json:
            print("\nPERHATIAN: Tabel berikut ada di Database MySQL TAPI BELUM DIDEFINISIKAN di file JSON:")
            for table_name in tables_in_db_but_not_in_json:
                print(f"  - {table_name}")
        
        if tables_defined_in_json_but_not_in_db:
            print("\nPERHATIAN: Tabel berikut didefinisikan di file JSON TAPI TIDAK DITEMUKAN di Database MySQL:")
            for table_name in tables_defined_in_json_but_not_in_db:
                print(f"  - {table_name}")

    print("\nVerifikasi selesai.")

if __name__ == "__main__":
    main()