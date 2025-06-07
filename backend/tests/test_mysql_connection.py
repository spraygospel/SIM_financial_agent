# test_mysql_connection.py
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv() # jika Anda sudah buat file .env untuk DB credential

try:
    mydb = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "your_root_password"), # Ganti dengan password Anda
        database=os.getenv("MYSQL_DATABASE", "ai_agent_erp_db") # Ganti jika nama DB beda
    )
    print("Koneksi ke MySQL berhasil!")
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES;") # Query sederhana
    for x in mycursor:
        print(x)
    mydb.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")