### **Dokumen Perencanaan Tambahan 11: Desain UI/UX dan Pengalaman Pengguna (v2)**

**Versi Dokumen**: 1.0
**Tanggal**: (Tanggal saat ini)
**Referensi Desain Visual**: Jules AI Interface (gambar State A: Planning & State B: Results)

---

## **Bab 1: Visi dan Filosofi Desain**

### **1.1. Pendahuluan**

Bab ini menetapkan visi tingkat tinggi dan prinsip-prinsip desain fundamental yang akan menjadi panduan dalam pengembangan antarmuka pengguna (UI) dan pengalaman pengguna (UX) untuk MVP AI Agent. Tujuannya bukan hanya menciptakan aplikasi yang fungsional, tetapi juga sebuah pengalaman yang terasa **canggih, profesional, dan dapat dipercaya**. Antarmuka ini adalah "wajah" dari kecerdasan agent kita, dan harus mampu mengkomunikasikannya secara efektif kepada semua pengguna, terutama calon investor.

### **1.2. Visi Utama Pengalaman Pengguna**

Visi kita adalah memberikan pengguna perasaan bahwa mereka sedang **berkolaborasi dengan seorang analis keuangan AI pribadi yang transparan, cerdas, dan sangat efisien.** Setiap interaksi harus memperkuat kepercayaan pengguna terhadap kemampuan dan akurasi agent.

Antarmuka ini harus mampu menerjemahkan kecanggihan teknis di balik layar (LangGraph, ORM, `DatabaseOperationPlan`) menjadi visualisasi proses yang intuitif dan mudah dipahami, bahkan oleh pengguna non-teknis sekalipun.

### **1.3. Ilustrasi Konsep Tata Letak Utama**

Sebagai gambaran awal, antarmuka kita akan mengadopsi tata letak tiga panel yang fleksibel, seperti diilustrasikan di bawah ini:

```ascii
+----------------------+------------------------------------------+--------------------------------+
| [<<] Sidebar Kiri    |    Area Interaksi Utama (Tengah)         | Panel Kanan (Data & Detail) [>>] |
|                      |                                          |                                |
| +------------------+ | +--------------------------------------+ | +----------+ +-----------+ +---+ |
| | [ ] Sesi Aktif   | | | Query Pengguna...                    | | | Data     | | Rencana   | |...| |
| +------------------+ | +--------------------------------------+ | +----------+ +-----------+ +---+ |
|                      |                                          |                                |
| Riwayat Query:       | +--------------------------------------+ | |                                |
| - Query 1  ✅      | | | [AI] Respons & Analisis Agent...     | | | (Konten Tab Aktif)         |
| - Query 2  🔄      | | |                                      | | |                                |
| - Query 3  ...     | | +--------------------------------------+ | |                                |
|                      |                                          |                                |
|                      | +--------------------------------------+ | |                                |
|                      | | [> Ketik pertanyaan Anda di sini...  ] | | |                                |
|                      | +--------------------------------------+ | |                                |
+----------------------+------------------------------------------+--------------------------------+
```

### **1.4. Filosofi Desain Fundamental**

Empat pilar filosofi akan menopang seluruh desain UI/UX kita:

**1. Profesional & Modern**
Antarmuka harus terlihat bersih, tajam, dan serius, layaknya alat analisis finansial kelas atas.
*   **Tema Gelap (Dark Mode):** Menggunakan latar belakang gelap dengan teks kontras tinggi untuk mengurangi kelelapan mata dan memberikan kesan premium.
*   **Tipografi Jelas:** Menggunakan jenis font sans-serif yang modern dan mudah dibaca.
*   **Ikon Minimalis:** Ikon harus intuitif dan tidak mengganggu alur visual.
*   **Tata Letak Terstruktur:** Penggunaan ruang yang efisien dan pengelompokan informasi yang logis untuk menghindari antarmuka yang terasa "penuh" atau berantakan.

**2. Transparansi Radikal (No Black Box)**
Ini adalah nilai jual utama kita. Pengguna harus selalu tahu apa yang sedang terjadi dan mengapa.
*   **Fase Perencanaan Terlihat:** Alih-alih hanya menampilkan ikon "loading", kita akan menampilkan **rencana aksi (To-do List)** yang dibuat oleh agent, lengkap dengan status pengerjaan setiap langkah secara real-time.
*   **Fase Hasil Terverifikasi:** Setiap analisis naratif yang dihasilkan harus didukung oleh **data mentah yang dapat diakses** di panel kanan. Ini membangun kepercayaan dan memungkinkan verifikasi.
*   **Logika Terbuka:** Dengan menampilkan `DatabaseOperationPlan` di salah satu tab, kita memberikan transparansi penuh (terutama untuk pengguna teknis/investor) tentang "cara berpikir" agent.

**3. Fokus pada Data & Insight**
Desain harus menempatkan informasi dan hasil analisis sebagai pusat perhatian.
*   **Prioritas Visual:** Ringkasan eksekutif dan narasi analisis harus menjadi hal pertama yang dilihat pengguna setelah proses selesai.
*   **Akses Data Mudah:** Tabel data mentah harus mudah diakses, interaktif (bisa di-sortir/filter), dan bisa diekspor.
*   **Fleksibilitas Tampilan:** Pengguna harus bisa menyembunyikan panel samping untuk fokus penuh pada data yang ditampilkan di area tengah.

**4. Interaksi yang Cerdas & Responsif**
Antarmuka harus terasa "hidup" dan cerdas, seolah-olah sedang berdialog dengan entitas yang benar-benar berpikir.
*   **Umpan Balik Real-Time:** Penggunaan animasi halus seperti **lingkaran status yang berdenyut (pulsing circle)** pada langkah yang sedang aktif memberikan umpan balik instan bahwa sistem sedang bekerja.
*   **Transisi yang Mulus:** Peralihan antara "Fase Perencanaan" (State A) dan "Fase Hasil" (State B) harus mulus dan tidak terasa terputus-putus.
*   **Status yang Informatif:** Setiap pesan status atau peringatan harus jelas, singkat, dan memberikan konteks kepada pengguna.

---



### **Dokumen Perencanaan Tambahan 11: Desain UI/UX dan Pengalaman Pengguna (v2)**

---

## **Bab 2: Peta Perjalanan Pengguna (User Journey Map)**

### **2.1. Pendahuluan**

Bab ini memetakan alur interaksi pengguna (user journey) secara lengkap, dari saat pengguna memiliki pertanyaan hingga mereka mendapatkan jawaban yang komprehensif dari AI Agent. Memahami perjalanan ini adalah kunci untuk merancang antarmuka yang intuitif dan memastikan setiap langkah memberikan nilai dan membangun kepercayaan. Perjalanan ini secara sadar dirancang untuk tidak memberikan jawaban instan, melainkan untuk melibatkan pengguna dalam proses "berpikir" agent, menjadikannya pengalaman yang transparan dan menarik.

### **2.2. Diagram Alur Perjalanan**

Diagram berikut mengilustrasikan alur utama yang akan dialami pengguna. Alur ini secara sengaja dibagi menjadi dua fase visual utama: **Fase Perencanaan (State A)** dan **Fase Hasil (State B)**.

```ascii
+-----------------------------------+
|             [ Mulai ]             |
| Pengguna memiliki pertanyaan bisnis |
+-----------------------------------+
                   |
                   v
+-----------------------------------+
|      Aksi Pengguna (Langkah 1)    |
| Mengetik & mengirimkan query      |
+-----------------------------------+
                   |
                   v
.-----------------------------------.
|   **Tampilan Fase Perencanaan**   |
|         **(State A)**             |  <-- Tampilan dari gambar referensi #2
| - Rencana Aksi (To-Do) muncul     |      (tampilan to-do list)
| - Indikator status aktif berdenyut|
'-----------------------------------'
                   |
                   v
+-----------------------------------+
|   Proses Agent Selesai            |
+-----------------------------------+
                   |
                   v
.-----------------------------------.
|       **Tampilan Fase Hasil**       |
|         **(State B)**             |  <-- Tampilan dari gambar referensi #1
| - Ringkasan & Narasi muncul       |      (tampilan 3 panel)
| - Data mentah tersedia di panel   |
'-----------------------------------'
                   |
                   v
+-----------------------------------+
|      Aksi Pengguna (Langkah 2)    |
| Menganalisis hasil atau mengajukan|
|         query berikutnya          |
+-----------------------------------+
                   |
                   +------> (Siklus kembali ke Langkah 1)
```

### **2.3. Deskripsi Naratif Setiap Langkah Perjalanan**

**Langkah 1: Inisiasi Query**
*   **Aksi Pengguna:** Pengguna membuka aplikasi dengan sebuah pertanyaan bisnis di benaknya. Misalnya, "Saya perlu tahu siapa saja customer yang piutangnya sudah jatuh tempo lebih dari 30 hari."
*   **UI State:** Aplikasi menampilkan antarmuka yang bersih, dengan fokus pada kotak input di bagian bawah Panel Tengah, siap menerima perintah. Riwayat percakapan sebelumnya (jika ada) terlihat di atasnya.

**Langkah 2: Input Query & Memulai Proses**
*   **Aksi Pengguna:** Pengguna mengetik pertanyaannya di kotak input dan menekan 'Enter' atau tombol 'Kirim'.
*   **UI State:**
    *   Query yang baru saja dikirim muncul di area interaksi sebagai "Blok Pertanyaan Pengguna".
    *   Kotak input menjadi non-aktif untuk sementara.
    *   Tepat di bawah blok pertanyaan, sebuah area baru untuk respons agent muncul.

**Langkah 3: Transisi ke Fase Perencanaan (State A)**
*   **Respon Sistem:** AI Agent menerima query, menganalisisnya, dan dengan cepat menghasilkan rencana aksi (To-do List).
*   **UI State:** Ini adalah momen kunci pertama. Alih-alih ikon loading biasa, pengguna akan melihat:
    *   **Judul Konfirmasi:** Sebuah judul singkat muncul, misal "Menganalisis Piutang Customer..."
    *   **Daftar Rencana Aksi:** Sebuah daftar bernomor yang jelas ditampilkan, contohnya:
        1.  `Memahami permintaan piutang...`
        2.  `Mengkonsultasikan skema data 'arbook' dan 'mastercustomer'...`
        3.  `Merencanakan query untuk data piutang...`
        4.  `Mengeksekusi query ke database...`
        5.  `Memvalidasi akurasi hasil...`
        6.  `Menyiapkan laporan akhir...`
    *   **Indikator Aktif:** Di samping langkah pertama (`Memahami permintaan...`), sebuah **lingkaran hijau yang berdenyut (pulsing circle)** muncul, menandakan inilah yang sedang dikerjakan agent.

**Langkah 4: Menyaksikan Agent Bekerja**
*   **Respon Sistem:** Agent mulai mengeksekusi setiap langkah dalam rencananya.
*   **UI State:** Pengguna dapat melihat progres secara visual dan real-time:
    *   Setelah langkah pertama selesai, lingkaran berdenyut menghilang dan digantikan ikon centang hijau (✅).
    *   Lingkaran hijau berdenyut kemudian muncul di samping langkah kedua, dan begitu seterusnya.
    *   Ini menciptakan pengalaman yang dinamis dan transparan, seolah-olah pengguna sedang melihat "checklist" agent dikerjakan satu per satu.

**Langkah 5: Transisi ke Fase Hasil (State B)**
*   **Respon Sistem:** Setelah semua langkah selesai (semua item di checklist sudah tercentang), agent selesai memproses dan telah menyiapkan laporan akhir.
*   **UI State:** Tampilan "Daftar Rencana Aksi" bertransisi dengan mulus (misalnya, dengan efek *fade out-fade in*) menjadi "Blok Respons Agent" yang berisi:
    *   **Ringkasan Eksekutif** di bagian atas.
    *   **Analisis Naratif** di bawahnya.
    *   Tombol ajakan bertindak seperti **"Lihat Data & Detail"**.

**Langkah 6: Interaksi dengan Hasil Analisis**
*   **Aksi Pengguna:** Pengguna membaca analisis. Merasa perlu verifikasi, ia mengklik tombol "Lihat Data & Detail".
*   **UI State:**
    *   Panel Kanan (yang mungkin tadinya ter-minimize) akan muncul atau menjadi fokus.
    *   Tab "Data Mentah" di Panel Kanan aktif secara default, menampilkan tabel data interaktif yang mendukung analisis tersebut.
    *   Pengguna dapat berinteraksi dengan tabel (sortir, cari) atau beralih ke tab lain seperti "Rencana Eksekusi (JSON)" untuk melihat detail teknis.

**Langkah 7: Siklus Selesai atau Melanjutkan Dialog**
*   **Aksi Pengguna:** Setelah puas dengan jawaban, pengguna kini bisa mengetik query lanjutan atau query baru di kotak input, yang sekarang sudah aktif kembali.
*   **UI State:** Sistem siap untuk memulai siklus perjalanan baru dari Langkah 2.

---

### **Dokumen Perencanaan Tambahan 11: Desain UI/UX dan Pengalaman Pengguna (v2)**

---

## **Bab 3: Anatomi Antarmuka Utama**

### **3.1. Pendahuluan**

Bab ini merinci anatomi atau tata letak utama dari antarmuka pengguna AI Agent. Desain ini mengadopsi pendekatan **tata letak tiga panel (three-panel layout)** yang telah terbukti efisien dalam banyak aplikasi berorientasi data dan pengembangan. Tujuannya adalah untuk memisahkan secara logis antara **navigasi/konteks sesi**, **area interaksi utama**, dan **area data pendukung/detail**, sambil memberikan fleksibilitas kepada pengguna untuk fokus pada area yang mereka butuhkan.

### **3.2. Ilustrasi Anatomi Antarmuka**

Berikut adalah ilustrasi ASCII art yang menggambarkan pembagian tiga panel utama dan komponen kunci di dalamnya:

```ascii
+================================++==============================================++======================================+
| PANEL KIRI (SIDEBAR)           ||           PANEL TENGAH (AREA INTERAKSI)      || PANEL KANAN (DATA & DETAIL)          |
| (Navigasi & Riwayat)           ||                                              || (Informasi Pendukung)                |
+================================++==============================================++======================================+
|                                ||                                              ||                                      |
|  [+] New Chat                  ||  +----------------------------------------+  ||   [Tab 1: Data] [Tab 2: Rencana]     |
|                                ||  | Blok Respons 1 (Query & Hasil)         |  ||                                      |
|  Sesi Aktif: session_xyz       ||  +----------------------------------------+  ||  +----------------------------------+  |
|  ----------------------------  ||                                              ||  |                                  |  |
|  Riwayat Query:                ||  +----------------------------------------+  ||  |                                  |  |
|   - "Tampilkan sales..." ✅    ||  | Blok Respons 2 (Fase Perencanaan)      |  ||  |       Konten Tab Aktif           |  |
|   - "Customer piutang..." 🔄   ||  +----------------------------------------+  ||  |                                  |  |
|                                ||                                              ||  |                                  |  |
|                                ||                                              ||  +----------------------------------+  |
|                                ||  +----------------------------------------+  ||                                      |
|                                ||  | [> Ketik pertanyaan di sini...]        |  ||                                      |
|                                ||  +----------------------------------------+  ||                                      |
|                                ||                                              ||                                      |
+--------------------------------++----------------------------------------------++--------------------------------------+
| [<<] Tombol Minimize Sidebar   ||                                              ||  [>>] Tombol Minimize Panel Kanan    |
+--------------------------------++----------------------------------------------++--------------------------------------+

```

### **3.3. Rincian Fungsi Setiap Panel**

**3.3.1. Panel Kiri: Sidebar Sesi & Riwayat**
*   **Peran**: Bertindak sebagai "papan navigasi" untuk seluruh percakapan. Ini membantu pengguna menjaga konteks dan dengan mudah meninjau kembali interaksi sebelumnya.
*   **Fungsi Utama**:
    *   **Manajemen Sesi**: Memungkinkan pengguna untuk memulai percakapan baru yang bersih, membersihkan konteks agent dari sesi sebelumnya.
    *   **Konteks Historis**: Memberikan daftar semua query yang telah diajukan dalam sesi saat ini, berfungsi sebagai "daftar isi" percakapan.
*   **Perilaku Interaktif**:
    *   **Dapat Di-minimize**: Pengguna dapat menyembunyikan panel ini untuk memberikan ruang lebih luas bagi Panel Tengah. Sebuah ikon `<<` atau ikon sidebar standar akan digunakan untuk fungsi ini. Saat di-minimize, panel ini bisa menjadi strip vertikal tipis dengan ikon untuk mengembalikannya.

**3.3.2. Panel Tengah: Area Interaksi Utama**
*   **Peran**: Ini adalah "panggung utama" tempat dialog antara pengguna dan AI Agent terjadi. Semua permintaan, proses perencanaan, dan hasil analisis tingkat tinggi ditampilkan di sini.
*   **Fungsi Utama**:
    *   **Input Pengguna**: Menyediakan antarmuka untuk memasukkan query.
    *   **Visualisasi Proses**: Menampilkan "Fase Perencanaan" (State A) untuk memberikan transparansi saat agent bekerja.
    *   **Penyajian Hasil**: Menampilkan "Fase Hasil" (State B) yang berisi ringkasan dan narasi yang mudah dicerna.
*   **Perilaku Interaktif**:
    *   Panel ini selalu terlihat dan merupakan fokus utama dari antarmuka. Lebarnya akan bertambah saat panel kiri dan/atau kanan di-minimize.
    *   Konten di dalamnya bersifat *scrollable*, memungkinkan pengguna untuk meninjau riwayat percakapan yang panjang.

**3.3.3. Panel Kanan: Panel Data & Detail**
*   **Peran**: Ini adalah "ruang lampiran" atau "ruang bukti" dari agent. Panel ini memenuhi prinsip **"Transparency First"** dengan menyediakan semua data mentah dan detail teknis yang mendukung hasil analisis.
*   **Fungsi Utama**:
    *   **Verifikasi Data**: Memungkinkan pengguna untuk melihat tabel data mentah yang digunakan agent, sehingga mereka dapat memvalidasi angka-angka dalam narasi.
    *   **Debugging & Wawasan Teknis**: Menyediakan akses ke `DatabaseOperationPlan` dan metrik performa, yang sangat berharga bagi pengguna teknis, tim developer, dan investor untuk memahami kecanggihan di balik layar.
    *   **Organisasi Informasi**: Menggunakan sistem tab untuk mengelompokkan berbagai jenis informasi pendukung agar tidak membuat pengguna kewalahan.
*   **Perilaku Interaktif**:
    *   **Dapat Di-minimize/Maximize**: Sama seperti Panel Kiri, panel ini dapat disembunyikan untuk memberikan fokus penuh pada Panel Tengah. Tombol kontrol (misalnya, ikon `>>` atau ikon panel) akan berada di pojok kanan atas atau di batas panel.
    *   **Konteks-Sensitif (Opsional)**: Konten di dalam panel ini (terutama tabel data) akan diperbarui secara dinamis sesuai dengan Blok Respons Agent mana yang sedang dilihat atau berinteraksi dengan pengguna di Panel Tengah.

---
Anatomi tiga panel ini memberikan keseimbangan antara kesederhanaan, kepadatan informasi, dan fleksibilitas, memungkinkan berbagai tipe pengguna (bisnis, teknis, investor) untuk mendapatkan tingkat detail yang mereka butuhkan dari AI Agent.
---

### **Dokumen Perencanaan Tambahan 11: Desain UI/UX dan Pengalaman Pengguna (v2)**

---

## **Bab 4: Rincian Komponen Tampilan (State A & State B)**

### **4.1. Pendahuluan**

Bab ini adalah inti dari dokumen desain, di mana kita membedah setiap komponen visual yang akan dilihat dan berinteraksi dengan pengguna. Pembahasan dibagi menjadi dua fase utama yang telah kita identifikasi dalam Peta Perjalanan Pengguna: **Fase Perencanaan (State A)** dan **Fase Hasil (State B)**.

---

### **4.2. Fase Perencanaan (State A): Agent Sedang "Berpikir"**

Tampilan ini muncul segera setelah pengguna mengirimkan query. Tujuannya adalah untuk menggantikan layar tunggu yang statis dengan visualisasi proses berpikir agent yang transparan dan menarik.

**4.2.1. Komponen: Daftar Rencana Aksi (To-do List)**
*   **Tujuan**: Untuk menunjukkan kepada pengguna langkah-langkah logis yang telah dirumuskan oleh agent untuk menjawab query mereka.
*   **Struktur Visual**: Sebuah daftar vertikal yang rapi, setiap item diberi nomor. Teks setiap item harus singkat dan dalam bahasa yang mudah dimengerti.
*   **Contoh Ilustrasi ASCII Art**:
    ```ascii
    +-------------------------------------------------------------+
    |  Menganalisis Piutang Customer...                           |
    |  ---------------------------------------------------------  |
    |                                                             |
    |  (1) [✅] Memahami permintaan piutang...                    |
    |  (2) [🔄] Mengkonsultasikan skema data relevan...           |  <-- Lingkaran hijau berdenyut
    |  (3) [ ] Merencanakan query untuk data piutang...             |
    |  (4) [ ] Mengeksekusi query ke database...                    |
    |  (5) [ ] Memvalidasi akurasi hasil...                         |
    |  (6) [ ] Menyiapkan laporan akhir...                          |
    |                                                             |
    +-------------------------------------------------------------+
    ```
*   **Konten Langkah-langkah**: Daftar langkah bersifat dinamis, namun untuk MVP, kita bisa menggunakan daftar standar yang mencerminkan node-node LangGraph:
    1.  `Memahami permintaan Anda...` (Node: `understand_query`)
    2.  `Mengkonsultasikan peta data...` (Node: `consult_schema`)
    3.  `Merencanakan pengambilan data...` (Node: `plan_execution`)
    4.  `Mengambil data dari database...` (Node: `execute_query`)
    5.  `Memverifikasi hasil...` (Node: `validate_results`)
    6.  `Menyusun laporan akhir...` (Node: `replace_placeholders`)

**4.2.2. Komponen: Indikator Status Langkah**
*   **Tujuan**: Memberikan umpan balik visual secara real-time tentang progres agent.
*   **Desain & Perilaku**:
    *   **Menunggu (Pending)**: Ikon lingkaran abu-abu kosong atau hanya nomor. Menandakan langkah ini belum dimulai.
    *   **Aktif (Active)**: **Lingkaran hijau yang berdenyut (pulsing green circle)** di samping teks langkah. Ini adalah elemen visual kunci yang menarik perhatian dan menunjukkan "di sinilah agent sekarang".
    *   **Selesai (Completed)**: Ikon centang hijau (✅) yang jelas. Menandakan langkah telah berhasil diselesaikan.
    *   **Gagal (Failed)**: Ikon silang merah (❌). Digunakan jika sebuah langkah gagal dan proses dihentikan.

---

### **4.3. Fase Hasil (State B): Laporan Telah Siap**

Tampilan ini menggantikan Fase Perencanaan setelah agent menyelesaikan semua tugasnya. Ini menyajikan hasil dengan cara yang terstruktur dan mudah dicerna, menggunakan tata letak tiga panel.

**4.3.1. Panel Kiri: Komponen Sidebar Riwayat**
*   **Tujuan**: Navigasi dan konteks sesi.
*   **Komponen**:
    *   **Tombol "New Chat"**: Tombol `[+]` yang jelas di bagian atas.
    *   **Daftar "Recent Queries"**: Setiap item dalam daftar adalah query pengguna yang bisa diklik. Saat diklik, Panel Tengah akan scroll ke blok respons yang sesuai.

**4.3.2. Panel Tengah: Komponen Blok Respons Agent**
*   **Tujuan**: Menyajikan inti dari jawaban agent.
*   **Struktur Visual**: Sebuah "kartu" atau blok konten yang terorganisir dengan baik.
*   **Komponen Internal**:
    1.  **Ringkasan Eksekutif (Executive Summary)**:
        *   Tampil di bagian paling atas blok.
        *   Menampilkan metrik kunci dengan angka yang besar dan label yang jelas.
        *   Contoh:
            ```
            Total Piutang      Jumlah Customer
            Rp 29.500.000      3 Customer
            ```
    2.  **Analisis Naratif (Analysis Narrative)**:
        *   Teks paragraf yang menjelaskan temuan utama, ditulis dalam bahasa alami.
        *   Angka-angka penting dalam narasi bisa dibuat tebal **(bold)**.
    3.  **Panel Kualitas & Validasi (Data Quality Panel)**:
        *   Sebuah baris atau area kecil di bawah narasi.
        *   Menampilkan **Skor Kualitas** (misalnya, `Kualitas Data: 95/100 ⭐⭐⭐⭐⭐`) dan **Peringatan** (misalnya, `⚠️ Note: Data hanya tersedia hingga 28 Jan 2023`).
    4.  **Tombol Aksi**: Tombol `[Lihat Data & Detail]` yang secara visual menonjol, mengundang pengguna untuk eksplorasi lebih lanjut.

**4.3.3. Panel Kanan: Komponen Panel Data Bertab**
*   **Tujuan**: Memberikan transparansi dan detail pendukung.
*   **Struktur Visual**: Sebuah kontainer dengan beberapa tombol tab di bagian atas.
*   **Komponen Tab**:
    1.  **Tab "Data Mentah"**:
        *   **Tampilan Default**.
        *   Menampilkan **tabel data interaktif**. Header kolom bisa diklik untuk sorting. Mungkin ada kotak pencarian kecil di atas tabel.
        *   Di pojok kanan atas tabel, ada tombol **[Ekspor CSV]**.
    2.  **Tab "Rencana Eksekusi"**:
        *   Menampilkan blok kode JSON yang diformat dengan baik dan *syntax-highlighted*.
        *   Menampilkan `DatabaseOperationPlan` yang digunakan untuk menghasilkan data. Ini menunjukkan "resep" yang dibuat agent.
    3.  **Tab "Log & Performa"**:
        *   Menampilkan daftar metrik performa sederhana.
        *   Contoh:
            *   `Waktu Proses Total: 4.2 detik`
            *   `Waktu Eksekusi Database: 1.5 detik`
            *   `Waktu Perencanaan AI: 2.1 detik`
            *   `Fallback Digunakan: Tidak`
    4.  **Tombol Maximize/Minimize Panel**: Sebuah ikon di pojok kanan atas seluruh panel (bukan hanya tabel) untuk menyembunyikan atau menampilkan panel ini.

---
Dengan merinci setiap komponen ini, tim frontend akan memiliki panduan yang sangat jelas untuk membangun antarmuka yang tidak hanya terlihat bagus tetapi juga secara fungsional mendukung semua fitur canggih dari AI Agent kita.
---

### **Dokumen Perencanaan Tambahan 11: Desain UI/UX dan Pengalaman Pengguna (v2)**

---

## **Bab 5: Spesifikasi Teknis untuk Frontend (API & Data)**

### **5.1. Pendahuluan**

Bab ini mendefinisikan "kontrak" data antara backend (FastAPI) dan frontend (React.js). Tujuannya adalah untuk merinci dengan jelas data apa yang harus disediakan oleh API backend agar frontend dapat me-render semua komponen UI yang telah kita rancang di Bab 4. Spesifikasi ini akan memandu pembuatan model Pydantic di `api_models.py` dan struktur state management di frontend.

### **5.2. Komunikasi Real-Time untuk Fase Perencanaan (State A)**

Untuk menciptakan pengalaman "live" di mana pengguna melihat progres agent secara real-time (langkah demi langkah), komunikasi satu arah dari server ke klien sangat ideal.

*   **Rekomendasi Teknologi**: **Server-Sent Events (SSE)**.
    *   **Mengapa SSE?**: SSE lebih sederhana untuk diimplementasikan baik di backend (FastAPI) maupun frontend dibandingkan WebSockets, dan sangat cocok untuk kasus penggunaan kita di mana kita hanya perlu "mendorong" pembaruan status dari server ke klien.
*   **Alur Komunikasi**:
    1.  Frontend mengirimkan query awal melalui `POST /api/v1/query`.
    2.  Backend menerima request, **langsung merespons dengan HTTP 202 Accepted** (atau respons awal lainnya) yang berisi `session_id`. Ini memberi tahu frontend, "Permintaan Anda saya terima dan sedang diproses."
    3.  Frontend, setelah menerima `session_id`, segera membuka koneksi SSE ke endpoint `GET /api/v1/stream_updates/{session_id}`.
    4.  Selama LangGraph workflow berjalan di backend, ia akan mem-publish *event* pembaruan status.
    5.  Backend mengirimkan *event* ini melalui koneksi SSE.
    6.  Frontend "mendengarkan" *event* ini dan memperbarui UI secara dinamis (misalnya, mengubah ikon status dari `[ ]` menjadi `[🔄]` lalu `[✅]`).
    7.  Ketika proses selesai, backend akan mengirim *event* terakhir yang berisi **seluruh hasil akhir (payload dari `QueryResponseSuccess`)**. Koneksi SSE kemudian bisa ditutup.

### **5.3. Struktur Data Event untuk SSE (`StreamUpdateEvent`)**

Setiap pembaruan yang dikirim melalui SSE akan memiliki struktur JSON yang konsisten.

*   **Contoh Event untuk Inisiasi Sesi (Guided Onboarding)**:
    *   Dikirim saat sesi baru dimulai untuk menampilkan sapaan dan saran query.
    ```json
    {
      "event_type": "SESSION_STARTED",
      "data": {
        "greeting_message": "Selamat pagi! Apa yang bisa saya bantu analisis hari ini?",
        "suggested_queries": [
          "Tampilkan total penjualan bulan ini",
          "Siapa 5 customer dengan piutang terbesar?",
          "Berapa stok produk X di gudang utama?"
        ]
      }
    }
    ```
*   **Contoh Event untuk Konfirmasi Pemahaman (Judul Fase Perencanaan)**:
    *   Dikirim tepat sebelum langkah-langkah perencanaan ditampilkan.
    ```json
    {
      "event_type": "AGENT_THINKING",
      "data": {
        "thought": "Menganalisis Piutang Customer..."
      }
    }
    ```
*   **Contoh Event untuk Pembaruan Langkah Perencanaan**:
    *   Dikirim untuk setiap perubahan status pada To-do list.
    ```json
    {
      "event_type": "PLANNING_STEP_UPDATE",
      "data": {
        "step_number": 2,
        "step_text": "Mengkonsultasikan peta data...",
        "status": "active" 
      }
    }
    ```
*   **Contoh Event untuk Hasil Akhir (Sukses)**:
    *   Dikirim setelah semua proses berhasil.
    ```json
    {
      "event_type": "FINAL_RESULT",
      "data": {
        // ... seluruh isi dari objek QueryResponseSuccess yang diperbarui ...
      }
    }
    ```
*   **Contoh Event untuk Error**:
    *   Dikirim jika terjadi error di mana pun dalam alur.
    ```json
    {
      "event_type": "WORKFLOW_ERROR",
      "data": {
        // ... seluruh isi dari objek QueryResponseError ...
      }
    }
    ```

### **5.4. Kebutuhan Data per Komponen UI dari API**

Berikut adalah rincian data yang dibutuhkan oleh setiap komponen utama di frontend, yang harus disediakan oleh backend melalui event `FINAL_RESULT` SSE.

**5.4.1. Panel Kiri (Sidebar)**
*   **Komponen**: `SessionHeader`, `RecentQueries`
*   **Kebutuhan Data**:
    *   `session_id`: `string`
    *   `conversation_history`: `Array<{ query: string, status: 'success' | 'failed' }>`
        *   Backend harus mengelola riwayat query dalam satu sesi dan mengirimkannya kembali agar frontend bisa me-render daftar "Recent Queries".

**5.4.2. Panel Tengah (Blok Respons Agent)**
*   **Komponen**: `ExecutiveSummary`, `AnalysisNarrative`, `DataQualityPanel`
*   **Kebutuhan Data**:
    *   `executive_summary`: `Array<{ metric_name: string, value: string, label: string }>`
    *   `final_narrative`: `string` (sudah diformat dengan HTML dasar jika perlu, misal `<b>...</b>`)
    *   `data_quality_score`: `number` (misal, 95)
    *   `warnings_for_display`: `Array<string>`

**5.4.3. Panel Kanan (Panel Data Bertab)**
*   **Komponen**: `RawDataTable`, `ExecutionPlanDisplay`, `PerformanceLog`
*   **Kebutuhan Data**:
    *   **Tab "Data Mentah"**:
        *   `data_table_for_display`: `Array<Object>` - Sebuah array dari objek JSON di mana setiap objek adalah satu baris data.
            *   **Penting**: Untuk tabel yang dinamis, backend juga harus menyediakan `column_headers: Array<{ key: string, label: string }>` agar frontend tahu urutan dan nama tampilan kolom.
    *   **Tab "Rencana Eksekusi"**:
        *   `database_operations_plan`: `Object` (atau string JSON yang sudah di-*prettify*) - Struktur JSON lengkap dari `DatabaseOperationPlan`.
    *   **Tab "Log & Performa"**:
        *   `performance_metrics`: `Object`
            *   Contoh: `{ "total_duration_sec": 4.2, "db_execution_sec": 1.5, "llm_planning_sec": 2.1, "fallback_used": false }`
        *   `mcp_tool_call_history`: `Array<Object>` (struktur `MCPToolCallLog` yang sudah kita definisikan). Ini bisa ditampilkan untuk debugging yang lebih mendalam.

### **5.5. Ringkasan Objek Respons API Final (`QueryResponseSuccess`)**

Berdasarkan semua kebutuhan di atas, objek `QueryResponseSuccess` yang dikirim dalam event `FINAL_RESULT` SSE harus memiliki struktur komprehensif sebagai berikut:

```typescript
// Contoh struktur dalam TypeScript untuk kejelasan di frontend

interface ExecutiveSummaryItem {
  metric_name: string;
  value: string;
  label: string;
}

interface ColumnHeader {
  key: string; // Nama field di objek data
  label: string; // Nama yang ditampilkan di UI
}

interface PerformanceMetrics {
  total_duration_sec: number;
  // ... metrik lainnya
}

interface ConfidenceLevel {
  level: 'High' | 'Medium' | 'Low';
  score: number; // Angka 0-100
  reason?: string; // Penjelasan singkat jika kepercayaan tidak tinggi
}

interface QueryResponseSuccess {
  session_id: string;
  final_narrative: string;
  executive_summary: ExecutiveSummaryItem[];
  
  // Untuk tabel data
  data_table_headers: ColumnHeader[];
  data_table_for_display: Array<Record<string, any>>;

  // Untuk panel kanan
  database_operations_plan: object; // atau string
  performance_metrics: PerformanceMetrics;

  // Metadata lain
  data_quality_score?: number;
  analysis_confidence: ConfidenceLevel; // <-- PENAMBAHAN DI SINI
  warnings_for_display?: string[];
}
```
Dokumen ini akan memastikan tim frontend dan backend bekerja dengan "kontrak" yang sama, mempercepat proses integrasi dan mengurangi potensi miskomunikasi.
---

### **Dokumen Perencanaan Tambahan 11: Desain UI/UX dan Pengalaman Pengguna (v2)**

---

## **Bab 6: Pertimbangan Tambahan & Iterasi Masa Depan**

### **6.1. Pendahuluan**

Bab ini berfungsi sebagai catatan untuk pengembangan di masa depan, setelah MVP berhasil diluncurkan. Merencanakan potensi peningkatan sejak awal akan membantu kita membangun fondasi (baik di backend maupun frontend) yang lebih mudah untuk dikembangkan dan diskalakan. Ini juga menunjukkan kepada calon investor bahwa kita memiliki visi jangka panjang untuk produk ini.

### **6.2. Responsivitas dan Tampilan di Berbagai Perangkat**

Meskipun MVP awal difokuskan pada pengalaman desktop (dengan tata letak tiga panel), kita harus mempertimbangkan bagaimana antarmuka ini akan beradaptasi pada layar yang lebih kecil seperti tablet atau bahkan ponsel.

*   **Rencana untuk Tablet**:
    *   Pada mode lanskap, tata letak tiga panel mungkin masih bisa dipertahankan.
    *   Pada mode potret, tata letak bisa berubah menjadi sistem satu kolom, di mana Panel Kiri dan Kanan menjadi *drawer* (laci) yang bisa ditarik keluar dari sisi layar atau diakses melalui tombol menu.
*   **Rencana untuk Ponsel**:
    *   Tata letak tiga panel tidak akan berfungsi. Antarmuka harus mengadopsi pendekatan **satu panel utama**.
    *   Panel Tengah (Area Interaksi) akan menjadi tampilan default.
    *   Riwayat sesi (Panel Kiri) akan diakses melalui ikon "menu hamburger" (☰).
    *   Panel Data & Detail (Panel Kanan) akan muncul sebagai *modal overlay* atau halaman terpisah setelah pengguna mengetuk tombol "Lihat Data & Detail".

### **6.3. Aksesibilitas (Accessibility - a11y)**

Untuk memastikan produk ini dapat digunakan oleh sebanyak mungkin orang, termasuk mereka yang memiliki keterbatasan, praktik aksesibilitas harus menjadi pertimbangan.

*   **Kontras Warna**: Pastikan kontras antara teks dan latar belakang di tema gelap memenuhi standar WCAG (Web Content Accessibility Guidelines) AA.
*   **Navigasi Keyboard**: Semua elemen interaktif (tombol, input, tab) harus dapat diakses dan dioperasikan hanya dengan menggunakan keyboard.
*   **Label ARIA**: Gunakan atribut ARIA (Accessible Rich Internet Applications) pada elemen-elemen dinamis untuk memberikan konteks kepada pembaca layar (screen readers). Misalnya, mengumumkan secara verbal saat status perencanaan berubah.
*   **Teks Alternatif**: Semua ikon yang tidak memiliki label teks harus memiliki teks alternatif.

### **6.4. Ide-ide Fitur UI/UX untuk Iterasi Masa Depan**

Berikut adalah beberapa ide fitur yang dapat meningkatkan pengalaman pengguna secara signifikan di versi-versi selanjutnya:

**6.4.1. Visualisasi Data Interaktif**
*   Di dalam Panel Kanan, tambahkan **Tab "Visualisasi"** baru.
*   Berdasarkan data yang diambil, agent bisa secara otomatis menghasilkan grafik sederhana (misalnya, diagram batang untuk perbandingan penjualan, diagram garis untuk tren waktu, atau diagram lingkaran untuk komposisi).
*   Pengguna dapat berinteraksi dengan grafik ini, seperti *hover* untuk melihat detail nilai.

**6.4.2. Personalisasi dan Pengaturan**
*   Memberikan pengguna kemampuan untuk menyesuaikan antarmuka mereka.
*   **Simpan Query Favorit**: Pengguna dapat menyimpan query yang sering mereka gunakan di Sidebar Kiri untuk akses cepat.
*   **Tema Tampilan**: Menambahkan pilihan tema terang (light mode) selain tema gelap.
*   **Pengaturan Notifikasi**: Mengatur bagaimana dan kapan pengguna menerima notifikasi.

**6.4.3. Fitur Kolaborasi**
*   **Bagikan Hasil (Share Results)**: Sebuah tombol untuk menghasilkan tautan unik ke hasil analisis tertentu, yang dapat dibagikan dengan anggota tim lain. Tautan tersebut akan membuka tampilan *read-only* dari laporan tersebut.
*   **Anotasi pada Laporan**: Kemampuan bagi pengguna untuk menambahkan komentar atau catatan pada narasi atau tabel data sebelum membagikannya.

**6.4.4. Umpan Balik Per-Respon (Feedback per Response)**
*   Di setiap "Blok Respons Agent", tambahkan ikon jempol ke atas (👍) dan jempol ke bawah (👎).
*   Ini akan memberikan data yang sangat berharga untuk melatih dan menyempurnakan model LLM serta logika agent di masa depan.

**6.4.5. Mode "Analisis Mendalam" (Deep Dive Mode)**
*   Jika pengguna tertarik pada satu metrik di Ringkasan Eksekutif (misalnya, "Total Piutang"), mereka dapat mengkliknya.
*   Agent kemudian akan secara otomatis menjalankan serangkaian query lanjutan yang relevan dengan metrik tersebut (misalnya, "Piutang berdasarkan umur", "Piutang per area penjualan", "Customer dengan piutang terbesar") dan menampilkannya sebagai analisis baru.

---
Dengan mencatat ide-ide ini sekarang, kita memastikan bahwa arsitektur yang kita bangun hari ini tidak akan membatasi kita untuk menambahkan fitur-fitur canggih dan menarik di masa depan. Ini melengkapi visi jangka panjang produk kita.