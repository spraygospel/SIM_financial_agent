import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
import datetime # Untuk menangani tipe data date/datetime saat mengambil sampel

# --- Konfigurasi ---
# Muat variabel lingkungan dari file .env di direktori backend
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

MYSQL_CONFIG = {
    'host': os.getenv("MYSQL_HOST", "localhost"),
    'user': os.getenv("MYSQL_USER", "root"),
    'password': os.getenv("MYSQL_PASSWORD"),
    'database': os.getenv("MYSQL_DATABASE")
}

# Jumlah baris sampel data yang ingin diambil per tabel
SAMPLE_DATA_LIMIT = 3 

# Daftar tabel yang ingin diabaikan (opsional, jika ada tabel sistem atau tidak relevan)
TABLES_TO_IGNORE = [
    # 'phinxlog', # Contoh tabel migrasi yang mungkin ingin diabaikan
    # 'users_system',
]

def format_sample_data_row(row_dict):
    """Format satu baris data sampel menjadi string yang lebih mudah dibaca."""
    formatted_items = []
    for key, value in row_dict.items():
        if isinstance(value, (datetime.date, datetime.datetime)):
            formatted_items.append(f"{key}: {value.isoformat()}")
        elif isinstance(value, bytes): # Menangani jika ada data BLOB/BINARY
            formatted_items.append(f"{key}: [binary_data_length_{len(value)}]")
        else:
            formatted_items.append(f"{key}: {value}")
    return ", ".join(formatted_items)

def get_mysql_schema_and_samples(connection):
    """
    Mengambil informasi skema dan beberapa baris data sampel dari database MySQL.
    Output berupa string yang diformat.
    """
    output_lines = []
    db_name = MYSQL_CONFIG['database']
    output_lines.append("DATABASE_SCHEMA_REPORT\n")
    output_lines.append(f"DATABASE_NAME: {db_name}\n")

    cursor = connection.cursor(dictionary=True)

    # Dapatkan daftar tabel
    cursor.execute("SHOW TABLES;")
    tables_data = cursor.fetchall()
    tables = [row[f"Tables_in_{db_name}"] for row in tables_data if row[f"Tables_in_{db_name}"] not in TABLES_TO_IGNORE]

    for table_name in tables:
        output_lines.append(f"---\nTABLE: {table_name}")

        # Dapatkan komentar tabel (jika ada)
        cursor.execute(f"""
            SELECT TABLE_COMMENT 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{table_name}';
        """)
        table_comment_result = cursor.fetchone()
        table_comment = table_comment_result['TABLE_COMMENT'] if table_comment_result and table_comment_result['TABLE_COMMENT'] else ""
        if table_comment:
            output_lines.append(f"COMMENT: {table_comment}")

        # Dapatkan detail kolom
        output_lines.append("COLUMNS:")
        # SHOW FULL COLUMNS FROM `table_name` diperlukan untuk mendapatkan Comment
        # Backticks di sekitar nama tabel untuk menangani nama tabel dengan spasi atau karakter khusus
        cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`;")
        columns = cursor.fetchall()
        column_details_list = []
        for col in columns:
            col_detail = (
                f"  - NAME: {col['Field']}, TYPE: {col['Type']}, "
                f"NULLABLE: {col['Null']}, KEY: {col['Key']}, "
                f"DEFAULT: {col['Default']}, EXTRA: {col['Extra']}, "
                f"COMMENT: {col['Comment'] if col['Comment'] else ''}"
            )
            column_details_list.append(col_detail)
        output_lines.extend(column_details_list)

        # Dapatkan foreign keys untuk tabel ini
        output_lines.append("FOREIGN_KEYS:")
        fk_query = f"""
            SELECT 
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME,
                CONSTRAINT_NAME
            FROM 
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE 
                TABLE_SCHEMA = '{db_name}' AND
                TABLE_NAME = '{table_name}' AND
                REFERENCED_TABLE_NAME IS NOT NULL;
        """
        cursor.execute(fk_query)
        fks = cursor.fetchall()
        if fks:
            for fk in fks:
                output_lines.append(
                    f"  - COLUMN: {fk['COLUMN_NAME']}, REFERENCES_TABLE: {fk['REFERENCED_TABLE_NAME']}, "
                    f"REFERENCES_COLUMN: {fk['REFERENCED_COLUMN_NAME']}, CONSTRAINT_NAME: {fk['CONSTRAINT_NAME']}"
                )
        else:
            output_lines.append("  (Tidak ada)")
            
        # Dapatkan beberapa sampel data
        output_lines.append(f"SAMPLE_DATA (LIMIT {SAMPLE_DATA_LIMIT}):")
        try:
            # Pastikan nama tabel juga di-escape dengan backticks di sini
            cursor.execute(f"SELECT * FROM `{table_name}` LIMIT {SAMPLE_DATA_LIMIT};")
            sample_rows = cursor.fetchall()
            if sample_rows:
                for row in sample_rows:
                    output_lines.append(f"  - {format_sample_data_row(row)}")
            else:
                output_lines.append("  (Tidak ada data sampel atau tabel kosong)")
        except mysql.connector.Error as err:
            output_lines.append(f"  (Error mengambil data sampel: {err})")
            
    cursor.close()
    return "\n".join(output_lines)

def main():
    if not MYSQL_CONFIG.get('password') or not MYSQL_CONFIG.get('database'):
        print("Error: Pastikan MYSQL_PASSWORD dan MYSQL_DATABASE sudah diatur di file .env pada direktori 'backend/'.")
        print("Contoh isi .env:")
        print("MYSQL_HOST=localhost")
        print("MYSQL_USER=your_user")
        print("MYSQL_PASSWORD=your_password")
        print("MYSQL_DATABASE=your_erp_database_name")
        return

    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        print(f"Berhasil terkoneksi ke MySQL database: {MYSQL_CONFIG['database']}\n")
        
        schema_report = get_mysql_schema_and_samples(connection)
        
        connection.close()
        
        # Simpan output ke file teks
        output_filename = f"{MYSQL_CONFIG['database']}_schema_report.txt"
        output_filepath = os.path.join(os.path.dirname(__file__), output_filename) # Simpan di direktori scripts
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(schema_report)
        
        print(f"\nLaporan skema dan sampel data berhasil dibuat dan disimpan di: {output_filepath}")
        print("Silakan copy-paste isi file tersebut ke dalam chat.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Username atau password MySQL salah.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Error: Database '{MYSQL_CONFIG['database']}' tidak ditemukan.")
        else:
            print(f"Error MySQL lainnya: {err}")
    except Exception as e:
        print(f"Terjadi error yang tidak terduga: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()