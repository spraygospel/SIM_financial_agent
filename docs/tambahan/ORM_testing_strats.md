
### **Dokumentasi Strategi Testing: Pendekatan Pembangunan Bertahap untuk ORM**

#### **1. Filosofi Inti: Membangun dari Pondasi, Bukan dari Atap**

Proyek kita, dengan 300+ tabel yang saling terhubung, ibarat membangun sebuah gedung pencakar langit yang sangat kompleks. Jika kita langsung mencoba memasang jendela di lantai 50 padahal pondasi dan kerangka di lantai 1 belum kokoh, seluruh bangunan akan runtuh.

Analogi Anda tentang membangun Lego pesawat atau rumah sangatlah tepat. Kesalahan kita di awal adalah mencoba "memasang body pesawat" (mengintegrasikan ORM ke agent) sebelum "memastikan setiap mur dan baut di kerangka mesin" (model dan relasi ORM) terpasang dengan benar. Akibatnya, kita harus terus-menerus "membongkar ulang" pekerjaan kita.

Oleh karena itu, strategi testing kita yang baru mengadopsi prinsip **pembangunan bertahap dari komponen terkecil dan paling fundamental, dengan validasi di setiap langkah sebelum melanjutkan ke langkah berikutnya.**

#### **2. Komponen dan Analogi Pembangunan**

| Komponen Proyek Kita        | Analogi Pembangunan Rumah/Lego                             | Status Saat Ini (untuk LLM berikutnya)      |
| --------------------------- | ---------------------------------------------------------- | ------------------------------------------- |
| **Definisi Model ORM**      | **Pondasi dan Tiang Pancang Rumah** atau **Blueprint Lego** | Sebagian besar sudah terdefinisi dan stabil |
| **Relasi Antar Model**      | **Besi Cor yang Menyambungkan Tiang** atau **Konektor Lego** | Sebagian besar sudah terdefinisi dan stabil |
| **Database Tes**            | **Tanah Kavling yang Bersih dan Rata**                     | Sudah disiapkan                               |
| **`setup_test_schema.py`**  | **Tim Konstruksi yang Membangun Pondasi**                  | Sudah dibuat dan berfungsi                 |
| **`TestDataFactory`**       | **Pabrik Otomatis yang Mencetak Bata & Semen**             | Sudah dibuat dan berfungsi                 |
| **File `test_orm_*.py`**    | **Inspektur Kualitas yang Menguji Kekuatan Tiap Pondasi**  | Sebagian sudah dibuat dan berhasil          |
| **Node `execute_query`**    | **Dinding dan Lantai Pertama Rumah**                       | Belum dibangun (STEP 3)                     |
| **Seluruh Alur LangGraph**  | **Rumah yang Utuh dengan Atap dan Interior**               | Belum dibangun (STEP 4-6)                   |
| **Frontend UI**             | **Pengecatan, Taman, dan Pagar Rumah**                     | Belum dibangun (STEP 7-8)                   |

#### **3. Alur Kerja Testing (Langkah-demi-Langkah)**

LLM yang akan melanjutkan proyek ini harus mengikuti alur kerja berikut dengan ketat:

**Fase 1: Memastikan Setiap Bagian Pondasi Sempurna (Fokus pada `db_models/` dan `tests/orm/`)**

Ini adalah fase di mana kita sekarang berada, dan ini adalah fase yang paling krusial.

1.  **Definisikan Satu Set Model Terkait (Satu Ruangan):**
    *   **Tugas:** Ambil satu modul bisnis (misalnya, `purchase_models.py`). Definisikan semua kelas model ORM untuk modul tersebut, lengkap dengan kolom, tipe data, dan `ForeignKey`.
    *   **Panduan:** Gunakan `sim_testgeluran_schema_report.txt` sebagai acuan mutlak untuk struktur kolom.

2.  **Definisikan Sambungan Antar Ruangan (`relationship`):**
    *   **Tugas:** Definisikan `relationship` di dalam model-model baru tersebut. Pastikan `back_populates` memiliki nama yang konsisten di kedua sisi relasi. **Selalu gunakan string untuk target `relationship`** (contoh: `relationship("PurchaseOrderH", ...)`).
    *   **Panduan:** Gunakan `metadata.txt` dan nama kolom untuk mengidentifikasi hubungan logis antar tabel.

3.  **Perbarui Pintu Masuk (`__init__.py`):**
    *   **Tugas:** Daftarkan semua kelas model baru di dalam file `backend/app/db_models/__init__.py`. Pastikan nama kelasnya ada di dalam list `__all__`.

4.  **Uji Cetak Biru (`generate_orm_blueprint.py`):**
    *   **Tugas:** Jalankan `python scripts/generate_orm_blueprint.py`.
    *   **Tujuan:** Untuk memastikan tidak ada `WARNING` atau error saat SQLAlchemy mencoba mengkonfigurasi semua model. Jika ada error, itu berarti ada masalah pada definisi model atau relasi di langkah 1 & 2. **Jangan lanjutkan sebelum skrip ini berjalan bersih.**

5.  **Bangun Ulang Pondasi di Lahan Tes (`setup_test_schema.py`):**
    *   **Tugas:** Jalankan `python tests/orm/setup_test_schema.py`.
    *   **Tujuan:** Untuk memastikan skema database tes kita berhasil dibuat ulang dari semua model ORM yang sudah kita definisikan. Jika ada `DatabaseError` di sini, itu berarti ada `ForeignKey` yang salah atau aturan database yang kita langgar. **Jangan lanjutkan sebelum skrip ini berhasil.**

6.  **Uji Kekuatan Ruangan Baru (Buat file `test_orm_purchase.py`):**
    *   **Tugas:** Buat file tes baru untuk modul yang baru saja dibuat. Buat fungsi tes yang terisolasi (seperti `test_purchase_order_creation`).
    *   **Metode:** Di dalam fungsi tes:
        a.  Mulai sesi database tes yang bersih.
        b.  Buat instance `TestDataFactory`.
        c.  Gunakan `factory.create("NamaModelBaru", ...)` untuk membuat data.
        d.  Jika ada kasus rumit (seperti *self-referencing NOT NULL*), buat data prasyaratnya secara manual di dalam fungsi tes itu sendiri.
        e.  Panggil `db.commit()`.
        f.  Lakukan query untuk mengambil data tersebut dan lakukan `assert` untuk memvalidasinya.
    *   **Tujuan:** Memastikan "Pabrik Data" kita bisa membuat model baru ini beserta semua dependensinya tanpa error.

7.  **Integrasikan ke Tes Utama (`run_all_orm_tests.py`):**
    *   **Tugas:** Impor dan panggil fungsi tes baru dari `run_all_orm_tests.py`.
    *   **Tujuan:** Memastikan penambahan tes baru tidak merusak tes-tes yang sudah ada.

**Hanya setelah satu modul (misalnya `purchase`) selesai didefinisikan dan diuji dengan 7 langkah di atas, barulah kita boleh beralih ke modul berikutnya (misalnya `production`).**

**Fase 2: Mendirikan Kerangka Utama (Fokus pada `langgraph_workflow/nodes/`)**

Fase ini baru akan dimulai **setelah SEMUA model ORM yang relevan untuk MVP telah melalui Fase 1.**

*   **Tugas:** Merefactor `execute_query_node` untuk menggunakan model-model ORM yang sudah teruji.
*   **Pengujian:** Membuat file tes baru (`tests/nodes/test_execute_query.py`) yang secara spesifik menguji node ini. Tes ini akan memberikan `DatabaseOperationPlan` buatan dan memverifikasi bahwa query SQLAlchemy yang dihasilkan sudah benar.

**Fase 3: Menyelesaikan dan Menginspeksi Bangunan (Fokus pada Tes End-to-End)**

*   **Tugas:** Menjalankan seluruh alur kerja dari API endpoint hingga ke database dan kembali.
*   **Pengujian:** Menggunakan Postman atau `TestClient` FastAPI untuk mengirim query dalam bahasa alami dan memverifikasi akurasi narasi serta tabel data yang dihasilkan.

Dengan mengikuti strategi pembangunan dan pengujian bertahap ini, kita memastikan setiap komponen kokoh sebelum kita membangun komponen lain di atasnya. Ini akan secara drastis mengurangi waktu "bongkar ulang" dan mempercepat penyelesaian proyek secara keseluruhan.