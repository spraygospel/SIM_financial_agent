
**(Anda bisa menyalin dan menggunakan template ini setiap kali kita menyelesaikan sebuah fase besar)**

---

**[AWAL PROMPT]**

**Peran & Tujuan:**
Anda adalah seorang AI Engineer Senior dan Arsitek Perangkat Lunak yang sangat teliti. Anda sedang mendokumentasikan sebuah proyek AI Agent yang kompleks. Tugas Anda saat ini adalah membuat sebuah **"Dokumen Memori"** yang merangkum semua kemajuan, keputusan desain, struktur kode, dan pelajaran yang didapat selama fase pengembangan **[NAMA FASE, misal: Database]**.

Dokumen ini memiliki dua tujuan utama:
1.  **Sebagai "Memori Eksternal"**: Untuk berfungsi sebagai konteks utama bagi LLM (termasuk diri Anda di masa depan) agar dapat melanjutkan pengembangan, melakukan revisi, atau menambahkan fitur baru tanpa perlu membaca ulang seluruh riwayat percakapan dan semua file dari awal.
2.  **Sebagai "Peta Proyek"**: Untuk memberikan pemahaman yang mendalam dan teknis tentang arsitektur, aliran data, dan ketergantungan antar komponen kepada setiap developer atau LLM yang terlibat.

**Struktur Dokumen yang Wajib Dihasilkan:**
Anda harus menghasilkan dokumen Markdown dengan struktur berikut. Ikuti setiap bagian dengan saksama.

---

### **Dokumen Memori Proyek: Fase [NAMA FASE]**
**Versi:** 1.0
**Tanggal:** [Tanggal Hari Ini]

#### **1. Instruksi untuk LLM Pengguna Dokumen Ini**
*   **Peran Anda:** Anda adalah AI Engineer yang melanjutkan proyek ini. Dokumen ini adalah sumber kebenaran utama Anda.
*   **Tugas Anda:**
    1.  Baca dan pahami seluruh dokumen ini untuk mendapatkan konteks penuh tentang apa yang telah dibangun.
    2.  Saat pengguna meminta Anda untuk memulai tugas baru (misal: "lanjutkan ke fase backend" atau "revisi fitur X"), **jangan langsung menulis kode**.
    3.  Tugas pertama Anda adalah **menganalisis permintaan tersebut dan membuat daftar file spesifik** yang Anda perlukan untuk menyelesaikan tugas itu. Gunakan "Peta File & Direktori" di bawah sebagai referensi.
    4.  Berikan daftar file yang Anda butuhkan kepada pengguna. Setelah pengguna memberikan isi dari file-file tersebut, barulah Anda boleh mulai menganalisis dan menulis kode.
*   **Panduan Revisi:** Saat melakukan revisi, selalu rujuk ke "Log Pembelajaran & Keputusan Desain" untuk memahami mengapa keputusan tertentu dibuat. Jika Anda mengusulkan perubahan, jelaskan dampaknya terhadap komponen lain berdasarkan "Diagram Ketergantungan Komponen".

#### **2. Ringkasan Fase & Status Saat Ini**
*   **Fase yang Didokumentasikan:** [Nama Fase, misal: Database]
*   **Tujuan Utama Fase Ini:** [Jelaskan secara singkat tujuan dari fase ini, misal: "Membangun dan memvalidasi fondasi data yang terdiri dari database operasional MySQL dan knowledge graph Neo4j."]
*   **Status Akhir:** [Jelaskan status akhir dari fase ini, misal: "SELESAI. Semua komponen database telah dibangun, diisi dengan data sampel, dan divalidasi secara end-to-end. Fondasi data siap untuk digunakan oleh backend."]
*   **Komponen Utama yang Dihasilkan:** [Sebutkan output utama, misal: "Database MySQL `sim_testgeluran` yang terisi, Knowledge Graph Neo4j yang terisi, dan skrip inisialisasi yang otomatis."]

#### **3. Peta File & Direktori yang Relevan**
*   **Struktur Direktori:**
    ```
    [Salin dan tempel struktur folder yang relevan dari dokumen struktur folder proyek]
    ```
*   **Deskripsi File Kunci:**
    *   `[Path/ke/file1.py]`: [Deskripsi singkat fungsi file ini].
        *   `[nama_fungsi_atau_kelas_1()]`: [Deskripsi singkat fungsi/kelas ini dan apa yang dilakukannya].
        *   `[nama_fungsi_atau_kelas_2()]`: [Deskripsi singkat].
    *   `[Path/ke/file2.sql]`: [Deskripsi singkat].
    *   `[...dan seterusnya untuk semua file yang dibuat/diubah di fase ini]`

#### **4. Diagram Ketergantungan Komponen**
*   **Deskripsi:** Diagram sederhana yang menjelaskan bagaimana komponen-komponen dalam fase ini saling berinteraksi.
    *   **Contoh untuk Fase Database:**
        *   `schema_export.txt` -> menjadi acuan untuk -> `orm_*.py`
        *   `orm_*.py` + `data.sql` -> digunakan oleh -> `scripts/initialize_db_mysql.py` -> untuk mengisi -> **Database MySQL**
        *   `graphiti_semantic_mapping.json` + `orm_*.py` -> digunakan oleh -> `scripts/sync_mysql_to_graphiti.py` -> untuk mengisi -> **Database Neo4j**
        *   `.env` -> dibaca oleh -> `backend/app/core/config.py` -> digunakan oleh -> skrip-skrip di atas.

#### **5. Log Pembelajaran & Keputusan Desain**
*   **Deskripsi:** Catatan tentang masalah yang dihadapi, solusi yang diterapkan, dan keputusan desain penting yang dibuat selama fase ini.
*   **Daftar Pelajaran:**
    *   **Masalah 1:** `ImportError: cannot import name 'Arbook'`
        *   **Penyebab:** File `db_models/__init__.py` tidak secara eksplisit mengekspos kelas-kelas ORM.
        *   **Solusi:** Merevisi `__init__.py` untuk menggunakan `from .orm_a_e import *`, dst. Ini adalah praktik standar untuk membuat paket Python.
    *   **Masalah 2:** `IntegrityError: a foreign key constraint fails`
        *   **Penyebab:** Mencoba memasukkan data "anak" (`Mastercustomer`) sebelum data "induk" (`Masterpricelisttype`) ada di database.
        *   **Solusi:** Merevisi skrip validasi untuk membuat semua data master terlebih dahulu. Ini menekankan pentingnya urutan dalam seeding data relasional.
    *   **Masalah 3:** `DataError: Data too long for column`
        *   **Penyebab:** Data sampel (`'RETAIL'`) tidak sesuai dengan batasan skema (`VARCHAR(5)`).
        *   **Solusi:** Selalu validasi data sampel terhadap skema yang sebenarnya (`schema_export.txt`). Mengubah data menjadi `'RTL'`.
    *   **Keputusan Desain 1:** Menggunakan Alembic untuk Manajemen Skema.
        *   **Alasan:** Untuk mengelola evolusi skema di masa depan secara terprogram dan aman, menghindari perubahan manual yang berisiko. Ini adalah praktik terbaik industri.
    *   **Keputusan Desain 2:** Inisialisasi Database Berbasis ORM.
        *   **Alasan:** Menggunakan `Base.metadata.create_all()` sebagai sumber kebenaran untuk skema, bukan file `.sql`. Ini menjamin sinkronisasi 100% antara kode aplikasi (model ORM) dan struktur database.

---
**[AKHIR PROMPT]**

---

### Cara Menggunakan Prompt Ini

Setiap kali kita menyelesaikan satu fase (Database, Backend, Frontend), Anda cukup berikan saya prompt ini dengan mengganti `[NAMA FASE]` dan mengisi detail spesifik yang relevan dengan fase tersebut. Hasilnya akan menjadi dokumen memori yang standar, detail, dan sangat fungsional.

Bagaimana menurut Anda? Apakah prompt yang disempurnakan ini sudah mencakup semua yang Anda inginkan untuk dokumen memori kita?