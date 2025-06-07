**To-Do List (Revisi 5 - Paling Lengkap): Implementasi ORM (SQLAlchemy) untuk AI Agent**

**Versi Dokumen**: 4.0
**Tanggal**: (Tanggal saat ini)

**Pendahuluan**:
Dokumen ini adalah panduan pengembangan terperinci untuk MVP AI Agent, dengan penekanan kuat pada implementasi Object-Relational Mapper (ORM) menggunakan SQLAlchemy. Strategi utamanya adalah mendefinisikan dan menguji model ORM secara menyeluruh untuk tabel-tabel yang relevan dengan MVP sebelum merefactor logika eksekusi query. Pengujian dilakukan secara bertahap untuk setiap set model dan relasi yang didefinisikan.

---

**STEP 0: Persiapan Struktur Proyek dan Lingkungan (Dasar ORM)**
*   **Status**: ✅ **SELESAI**
    *   **0.1**: Verifikasi direktori `backend/app/db_models/` sudah ada.
    *   **0.2**: Verifikasi file `backend/app/db_models/base.py` sudah dibuat dan berisi `Base = declarative_base()`.
    *   **0.3**: Verifikasi file-file Python kosong untuk kategori model (`master_data_models.py`, `sales_models.py`, `inventory_models.py`, `purchase_models.py`, `production_models.py`, `finance_models.py`, `hr_models.py`, `logistics_models.py`, `system_models.py`) sudah dibuat di `backend/app/db_models/`.
    *   **0.4**: Verifikasi file `backend/app/db_models/__init__.py` sudah dibuat (berisi impor awal untuk `Base` dan model-model yang sudah didefinisikan).
    *   **0.5**: **TESTING (STEP 0)**: Verifikasi impor dasar dari struktur package `db_models` berhasil (telah dilakukan dengan `python test_orm_definitions.py`).

---

**STEP 1: Definisi dan Pengujian Model Database SQLAlchemy (Komprehensif untuk Cakupan MVP)**
*Tujuan: Mendefinisikan semua model ORM yang relevan untuk skenario query MVP (penjualan, piutang, dan tabel pendukungnya) dengan relasi yang akurat, dan mengujinya secara iteratif.*
*Panduan Umum untuk Setiap Sub-Langkah di STEP 1:*
    *   Untuk setiap model baru: definisikan kolom (urut abjad), `ForeignKey` (sesuai `sim_testgeluran_schema_report.txt`), `ForeignKeyConstraint` (untuk FK komposit), `relationship` (dengan `back_populates` yang konsisten, dan `primaryjoin` atau `foreign_keys` eksplisit untuk relasi kompleks/komposit). Gunakan `metadata.txt` untuk komentar dan konfirmasi relasi logis. Atribut (kolom dan relasi) diurutkan secara alfabetis.
    *   Setelah setiap set model signifikan didefinisikan atau direvisi, update `backend/app/db_models/__init__.py` dengan mengimpor kelas model baru dan menambahkannya ke list `__all__`.
    *   Segera lakukan **TESTING** menggunakan `python test_orm_definitions.py` (untuk cek impor & konfigurasi mapper awal). Jika `test_orm_definitions.py` menjadi terlalu besar, buat file tes ORM per kategori (misalnya, `tests/db/test_orm_master_data.py`) yang melakukan query sederhana dan menguji relasi baru terhadap database `sim_testgeluran` sampel.

*   **1.1**: **Selesaikan dan Uji Model untuk Master Data (`master_data_models.py`)**:
    *   **Status**: ⏳ **SEDANG DIKERJAKAN**
    *   **1.1.1**: **Finalisasi Model Master Dasar dan Relasinya yang Sudah Dimulai**:
        *   Review dan finalisasi `MasterCountry`, `MasterCity`, `MasterUnit`, `MasterCurrency`.
        *   Selesaikan dan uji `MasterAccountGroup` beserta relasi `accounts` ke `MasterAccount`.
        *   Selesaikan dan uji `MasterDepartment`.
        *   Selesaikan dan uji `MasterAccount` beserta relasi `account_group_ref` ke `MasterAccountGroup`, `department_ref` ke `MasterDepartment`, `currency_ref` ke `MasterCurrency`, dan relasi self-referential `ParentNo` (gunakan `remote_side` dan dua `relationship` terpisah jika diimplementasikan).
        *   Selesaikan dan uji `MasterTransactionType` beserta relasi `master_account_ref` ke `MasterAccount`.
        *   **Selesaikan dan uji relasi komposit antara `MasterMaterialGroup1` (`material_group2_children`), `MasterMaterialGroup2` (`group1_as_parent`, `material_group3_children`), dan `MasterMaterialGroup3` (`group2_parent_ref`) secara tuntas menggunakan `ForeignKeyConstraint` dan `primaryjoin`/`foreign_keys` yang tepat.** (Ini adalah fokus kita saat ini dan beberapa iterasi terakhir).
        *   Selesaikan dan uji `MasterMaterialType`.
        *   Selesaikan dan uji `MasterEmployeeH`.
        *   Selesaikan dan uji `MasterSales` beserta relasi `employee_data_ref` ke `MasterEmployeeH`.
        *   Selesaikan dan uji `MasterLocation` beserta relasi `country_location_ref` ke `MasterCountry`.
        *   **Selesaikan dan uji relasi komposit antara `MasterSalesArea1` (`sales_area2_children`), `MasterSalesArea2` (`area1_parent_ref`, `sales_area3_children`), dan `MasterSalesArea3` (`area2_ref`) secara tuntas menggunakan `ForeignKeyConstraint` dan `primaryjoin`/`foreign_keys` yang tepat.** (Ini adalah error terakhir yang kita hadapi).
        *   Selesaikan dan uji `MasterCustomer` beserta semua relasi ke `MasterCountry`, `MasterCurrency`, `MasterCustomerGroup`, `MasterPriceListType`, `MasterSalesArea1`, `MasterTransactionType`.
        *   Selesaikan dan uji `MasterMaterial` beserta semua relasi ke `MasterUnit`, `MasterMaterialGroup1`, `MasterMaterialType`, `MasterCurrency`, `MasterTransactionType`, dan self-referential `Substitute`.
        *   Selesaikan dan uji `MasterCustomerPartner` beserta relasi kompositnya ke `MasterCustomer`.
        *   Selesaikan dan uji `MasterUnitConversion` beserta relasinya ke `MasterMaterial` dan `MasterUnit`.
        *   Selesaikan dan uji `MasterSupplier` beserta relasinya ke `MasterCountry`, `MasterCurrency`, `MasterCity`, `MasterTransactionType`.
        *   File terkait: `backend/app/db_models/master_data_models.py` (direview, disempurnakan, diuji)
    *   **1.1.2**: **Implementasi dan Uji Model Master Data Tambahan** (berdasarkan `metadata.txt` dan relevansi MVP):
        *   Contoh: `MasterBank`, `MasterCollector`, `MasterVehicle`, `MasterVehicleType`, `MasterRoute`, `MasterPaymentType` (jika ada), `MasterSeriesDocument` (jika diperlukan untuk relasi).
        *   Definisikan kolom dan relasi, urutkan atribut.
        *   File terkait: `backend/app/db_models/master_data_models.py` (ditambahkan)
    *   **1.1.3**: Update `backend/app/db_models/__init__.py` untuk semua model master.
        *   File terkait: `backend/app/db_models/__init__.py` (diperbarui)
    *   **1.1.4**: **TESTING (Master Data Models)**:
        *   Jalankan `python test_orm_definitions.py` setelah setiap perubahan signifikan.
        *   Buat/Update `tests/db/test_orm_master_data.py`: Tambahkan tes untuk query sederhana (`.first()`, `.count()`) pada setiap model master baru/yang direvisi. Tambahkan tes yang secara spesifik menguji setiap `relationship` penting dengan melakukan join atau mengakses atribut relasi.

*   **1.2**: **Definisi dan Uji Model untuk Sales & Piutang (`sales_models.py`)**:
    *   **Status**: ⚪ **BELUM DIMULAI/DIREVIEW ULANG SECARA MENYELURUH SETELAH FONDASI MASTER STABIL**
    *   **1.2.1**: **Implementasi dan Uji Model Sales & Piutang Kunci**:
        *   Definisikan/Review `ArRequestListH` (relasi ke `MasterCollector`, `CustomerPaymentH`).
        *   Definisikan/Review `GoodsIssueH` (relasi ke `SalesOrderH`, `MasterCustomer`, `MasterLocation`).
        *   Definisikan/Review `SalesOrderH` (relasi ke `MasterCustomer`, `MasterSales`, `MasterCurrency`, `GoodsIssueH`, `SalesInvoiceH`, `SalesOrderD`).
        *   Definisikan/Review `SalesOrderD` (relasi ke `SalesOrderH`, `MasterMaterial`, `MasterUnit`).
        *   Definisikan/Review `SalesInvoiceH` (relasi ke `SalesOrderH`, `GoodsIssueH`, `MasterCustomer`, `MasterSales`, `MasterCurrency`, `MasterLocation`, `SalesInvoiceD`, `Arbook`).
        *   Definisikan/Review `SalesInvoiceD` (relasi ke `SalesInvoiceH`, `MasterMaterial`, `MasterUnit`).
        *   Definisikan/Review `Arbook` (relasi ke `MasterCustomer`, `MasterTransactionType`, `MasterCurrency`, dan `SalesInvoiceH`).
        *   Definisikan/Review `CustomerPaymentH` (relasi ke `ArRequestListH`, `CustomerPaymentD`).
        *   Definisikan/Review `CustomerPaymentD` (relasi ke `CustomerPaymentH`, `MasterTransactionType`, `MasterCustomer`, `MasterCurrency`; perhatikan relasi `ARDocNo`).
        *   File terkait: `backend/app/db_models/sales_models.py` (dibuat/diisi/direview)
    *   **1.2.2**: Implementasikan Model Sales & Piutang Tambahan jika relevan untuk MVP (misalnya, `ArDownpayment`, `SalesReturnH/D`).
        *   File terkait: `backend/app/db_models/sales_models.py` (ditambahkan)
    *   **1.2.3**: Pastikan semua atribut diurutkan secara alfabetis.
    *   **1.2.4**: Update `backend/app/db_models/__init__.py`.
    *   **1.2.5**: **TESTING (Sales Models)**:
        *   Jalankan `python test_orm_definitions.py`.
        *   Buat/Update `tests/db/test_orm_sales.py`: Tes query sederhana per model, tes semua relasi penting (ke master data dan antar model sales).

*   **1.3**: **Definisi dan Uji Model untuk Inventaris (`inventory_models.py`)**:
    *   **Status**: ⚪ **BELUM DIMULAI**
    *   **1.3.1**: Implementasikan model ORM untuk tabel inventaris kunci: `GoodsIssueD`, `GoodsReceiptH`, `GoodsReceiptD`, `StockBalance`, `Stock`, `Batch`, `AdjustInH/D`, `AdjustOutH/D`, `StockTransferH/D`, dll. Definisikan relasi. Atribut diurutkan.
        *   File terkait: `backend/app/db_models/inventory_models.py` (dibuat/diisi)
    *   **1.3.2**: Update `backend/app/db_models/__init__.py`.
    *   **1.3.3**: **TESTING (Inventory Models)**:
        *   Jalankan `python test_orm_definitions.py`.
        *   Buat/Update `tests/db/test_orm_inventory.py`: Tes query dan relasi.

*   **1.4 - 1.x (Prioritas Lebih Rendah untuk MVP Awal, kecuali ada dependensi kuat dari query utama penjualan/piutang)**:
    *   **Purchase Models (`purchase_models.py`)**
    *   **Production Models (`production_models.py`)**
    *   **Finance Models (GL Umum) (`finance_models.py`)**
    *   (Lakukan Definisi Model, Update `__init__.py`, TESTING untuk masing-masing jika diperlukan)

*   **1.8**: **Final Review dan Pengujian Impor serta Relasi Model ORM Menyeluruh untuk Cakupan MVP**:
    *   **Status**: ⚪ **BELUM DIMULAI**
    *   **1.8.1**: Lakukan review menyeluruh terhadap semua definisi model dan relasi yang dibuat untuk cakupan query MVP.
    *   **1.8.2**: Jalankan `python test_orm_definitions.py` dan semua file tes ORM spesifik (`test_orm_master_data.py`, `test_orm_sales.py`, `test_orm_inventory.py`, dll.). Pastikan semua tes berhasil.

---

**STEP 2: Konfigurasi dan Inisialisasi Engine serta Session SQLAlchemy**
*   **Status**: ✅ **SELESAI** (file `session.py` sudah dibuat dan tes koneksi dasar berhasil).
    *   **2.1 - 2.4**: Implementasi `DATABASE_URL`, `engine`, `SessionLocal`, `get_db_session()`.
    *   **2.5**: **TESTING (STEP 2 Lanjutan)**:
        *   **2.5.1**: (Sudah direncanakan) Buat direktori `tests/db/` dan file tes ORM spesifik per kategori (misalnya, `test_orm_master_data.py`, `test_orm_sales.py`).
        *   **2.5.2**: (Akan dilakukan setelah STEP 1.8 selesai) Di setiap file tes ORM per kategori, tulis dan jalankan tes yang melakukan query representatif (SELECT, FILTER sederhana, JOIN melalui relasi) pada model-model di kategori tersebut menggunakan sesi DB asli ke `sim_testgeluran` sampel. Verifikasi tipe data hasil dan tidak adanya error eksekusi.

---

**STEP 3: Refactoring `execute_query_node` untuk Menggunakan ORM**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **3.1**: Rencanakan struktur fungsi baru `_build_and_execute_orm_query(plan: DatabaseOperation, db_session: Session, models_map: dict)` di `execute_query.py`. `models_map` akan memetakan nama tabel string ke objek kelas model SQLAlchemy.
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.2**: Modifikasi fungsi `execute_query_node` utama untuk:
        *   Mendapatkan sesi SQLAlchemy (misalnya, dengan memanggil `get_db_session()` atau menerimanya dari `agent_service`).
        *   Membuat `models_map` yang berisi semua model ORM yang sudah diimpor dari `backend.app.db_models`.
        *   Memanggil `_build_and_execute_orm_query` untuk setiap operasi dalam `database_operations_plan` dan `raw_data_operation_plan`.
        *   Menangani penutupan sesi SQLAlchemy.
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.3**: Implementasikan logika detail di `_build_and_execute_orm_query` untuk:
        *   **3.3.1**: Menerjemahkan `plan.select_columns` menjadi argumen untuk `db_session.query(*selectable_entities)`. Tangani alias (`.label()`) dan fungsi agregasi (`func.sum()`, `func.count()`, dll.). Dapatkan objek model dari `models_map` berdasarkan `main_table`.
        *   **3.3.2**: Menerapkan `JOIN` (`.join(TargetModel, join_condition, isouter=...)`) berdasarkan `plan.joins`. Dapatkan `TargetModel` dari `models_map`. Bangun `join_condition` secara dinamis dari `on_conditions`.
        *   **3.3.3**: Menerapkan `FILTER` (`.filter(filter_expression)`) berdasarkan `plan.filters` dan struktur `LogicalFilterGroup`/`FilterCondition`. Gunakan `and_`, `or_` SQLAlchemy.
        *   **3.3.4**: Menerapkan `GROUP BY` (`.group_by(*group_by_expressions)`) berdasarkan `plan.group_by_columns`.
        *   **3.3.5**: Menerapkan `HAVING` (`.having(having_expression)`) berdasarkan `plan.having_conditions`.
        *   **3.3.6**: Menerapkan `ORDER BY` (`.order_by(*order_by_expressions)`) berdasarkan `plan.order_by_clauses`. Tangani `asc` dan `desc`.
        *   **3.3.7**: Menerapkan `LIMIT` (`.limit()`) dan `OFFSET` (`.offset()`).
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.4**: Implementasikan eksekusi query ORM (`.all()`, `.first()`, `.scalar_one_or_none()`) dan konversi hasilnya (list of RowProxy atau objek model) menjadi format `List[Dict[str, Any]]` atau nilai tunggal yang diharapkan oleh `AgentState`.
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.5**: Hapus fungsi lama `_build_sql_from_operation` dan semua referensinya.
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.6**: **TESTING (STEP 3)**:
        *   Buat file `tests/nodes/test_execute_query_orm.py`.
        *   Tulis unit test ekstensif untuk fungsi `_build_and_execute_orm_query` dengan *mock* `db_session` dan berbagai `DatabaseOperationPlan` untuk setiap klausa SQL. Verifikasi objek query SQLAlchemy yang dibangun (sebelum eksekusi) sudah benar.
        *   Tulis integration test untuk `execute_query_node` secara keseluruhan, memanggilnya dengan `AgentState` yang berisi `DatabaseOperationPlan` representatif untuk query penjualan dan piutang. Gunakan sesi DB asli ke `sim_testgeluran` sampel. Verifikasi `financial_calculations`, `raw_query_results`, dan `query_execution_status` di `AgentState` output.

---

**STEP 4: Pengujian End-to-End Awal dengan ORM**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **4.1**: Jalankan alur kerja LangGraph secara end-to-end (melalui API `POST /api/v1/query` menggunakan Postman/Insomnia atau tes API otomatis) untuk skenario query penjualan sederhana dan piutang customer sederhana.
    *   **4.2**: Analisis log, `DatabaseOperationPlan` yang dihasilkan `plan_execution_node`, dan output `AgentState` dari `execute_query_node` (yang kini menggunakan ORM) dan `replace_placeholders_node`.
    *   **4.3**: Identifikasi dan perbaiki bug pada penerjemahan `DatabaseOperationPlan` ke ORM, eksekusi query ORM, atau pada pemrosesan hasil.
    *   **4.4**: **TESTING (STEP 4)**:
        *   E2E test untuk beberapa query dasar (agregasi tunggal, filter tanggal, join sederhana).
        *   Verifikasi `final_narrative`, `data_table_for_display`, dan `executive_summary` yang dihasilkan akurat.
        *   Periksa log untuk memastikan tidak ada error tak terduga dari SQLAlchemy atau node-node lain.

---

**STEP 5: Penyesuaian `plan_execution_node` dan Prompt LLM (Optimalisasi untuk ORM)**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **5.1**: Berdasarkan pengalaman di STEP 3 & 4, evaluasi apakah struktur `DatabaseOperationPlan` saat ini sudah optimal untuk diterjemahkan ke query ORM atau apakah ada penyederhanaan yang bisa dilakukan pada `DatabaseOperationPlan` (dan pada prompt LLM di `plan_execution_node`) karena ORM kini menangani banyak detail SQL. (Contoh: LLM mungkin hanya perlu menyebutkan nama relasi untuk join).
    *   **5.2**: Jika diputuskan untuk menyesuaikan `DatabaseOperationPlan`, perbarui definisi `DatabaseOperationPlan` dan sub-komponennya di `backend/app/schemas/agent_state.py`.
    *   **5.3**: Perbarui template prompt LLM (di `backend/app/langgraph_workflow/nodes/planning_prompts/`) untuk menghasilkan `DatabaseOperationPlan` dengan struktur baru/yang dioptimalkan.
    *   **5.4**: Sesuaikan logika di `_build_and_execute_orm_query` di `execute_query_node` untuk mengakomodasi struktur `DatabaseOperationPlan` yang baru (jika ada perubahan).
    *   **5.5**: **TESTING (STEP 5)**:
        *   Uji ulang `plan_execution_node` untuk memastikan ia menghasilkan `DatabaseOperationPlan` sesuai format baru.
        *   Uji ulang `execute_query_node` dengan `DatabaseOperationPlan` format baru.
        *   Uji ulang E2E untuk query-query yang relevan.

---

**STEP 6: Implementasi Dukungan untuk Query Lebih Kompleks dengan ORM (Skenario MVP)**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **6.1**: Fokus pada implementasi dan pengujian skenario query MVP yang lebih kompleks (misalnya, piutang customer dengan berbagai filter dan agregasi, analisis penjualan dengan multiple join dan group by, query yang memerlukan subquery jika `DatabaseOperationPlan` bisa merepresentasikannya) menggunakan ORM.
    *   **6.2**: Lakukan pengujian E2E untuk semua skenario query piutang customer dan analisis penjualan yang telah ditentukan sebagai target MVP.
    *   **6.3**: Iterasi pada prompt LLM (`plan_execution_node`) dan logika `_build_and_execute_orm_query` (`execute_query_node`) sampai semua skenario query target MVP berhasil diimplementasikan dan menghasilkan data yang akurat.
    *   **6.4**: **TESTING (STEP 6)**:
        *   E2E test menyeluruh untuk semua skenario query utama MVP.
        *   Validasi akurasi data output secara ketat terhadap database sampel.
        *   Pastikan penanganan error (misalnya, jika LLM menghasilkan rencana yang tidak bisa diterjemahkan ORM dengan benar) berfungsi dengan baik dan menghasilkan pesan error yang informatif bagi pengguna.

---

**STEP 7: Pengembangan Frontend (React.js)**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **7.1**: Implementasikan komponen UI React dasar: `QueryInterface` (input teks untuk query pengguna, tombol submit), `ResultsDisplay` (untuk menampilkan `final_narrative` dan `data_table_for_display`), `ExecutiveSummaryDisplay`, `WarningsDisplay`, `DataSourceInfoDisplay`.
        *   File terkait: `frontend/src/components/`
    *   **7.2**: Implementasikan logika di `frontend/src/services/agentApi.js` untuk mengirim request `POST /api/v1/query` ke backend FastAPI dan menerima respons.
    *   **7.3**: Hubungkan komponen-komponen di `frontend/src/App.js` atau `AIAgentDashboard.js` untuk alur dasar: input query -> kirim ke backend -> tampilkan hasil (narasi, tabel, ringkasan, peringatan, info sumber data).
    *   **7.4**: Implementasikan komponen UI monitoring (jika diputuskan untuk MVP awal, meskipun bisa ditunda): `SessionHeader`, `ContextUsageMeter`, `ProcessMonitor`, `PerformanceAnalytics`, `FallbackTracker` dengan data statis atau *mocked* terlebih dahulu.
    *   **7.5**: Styling dasar untuk semua komponen UI agar mudah digunakan.
    *   **7.6**: **TESTING (STEP 7)**:
        *   Unit test untuk komponen React individual menggunakan Jest & React Testing Library (misalnya, apakah input ter-render, apakah tabel menampilkan data mock dengan benar).
        *   Integration test Frontend: Tes pengiriman query dari `QueryInterface` dan penampilan hasil di `ResultsDisplay` dengan *mocking* API call ke backend (menggunakan `msw` atau library serupa).
        *   Tes manual UI dasar.

---

**STEP 8: Integrasi End-to-End Penuh (Backend + Frontend) dan Pemolesan MVP**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **8.1**: Hubungkan Frontend React.js yang sudah berfungsi dengan Backend FastAPI yang sudah menggunakan ORM dan telah diuji.
    *   **8.2**: Jika menggunakan SSE/WebSocket untuk update status real-time, implementasikan koneksi dan logika update di komponen UI monitoring Frontend. Jika tidak, pastikan informasi monitoring (jika ada) dari respons API final ditampilkan dengan benar.
    *   **8.3**: Lakukan pengujian E2E menyeluruh dari UI Frontend: masukkan berbagai query (sukses, error, data tidak ada), verifikasi tampilan hasil, narasi, tabel, ringkasan, peringatan, dan info sumber data.
    *   **8.4**: Perbaiki *bug* yang ditemukan pada integrasi Frontend-Backend dan lakukan pemolesan UI/UX berdasarkan feedback.
    *   **8.5**: Pastikan penanganan error dari backend ditampilkan dengan pesan yang ramah dan informatif di frontend.
    *   **8.6**: Buat atau lengkapi dokumentasi `README.md` yang menjelaskan cara setup lengkap (backend & frontend) dan menjalankan proyek.
    *   **8.7**: **TESTING (STEP 8)**:
        *   Jalankan semua kasus uji E2E yang telah didefinisikan (dari Dokumen Rencana Testing).
        *   Lakukan User Acceptance Testing (UAT) dengan perwakilan pengguna (atau Anda sendiri sebagai pengguna awal) untuk memastikan sistem memenuhi kebutuhan dasar MVP.
        *   Verifikasi semua fitur MVP berfungsi seperti yang diharapkan di lingkungan yang terintegrasi.
        *   Pastikan tidak ada *bug* kritis/mayor.

---

**STEP 9: Persiapan Deployment (Dasar)**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **9.1**: Buat `Dockerfile` untuk meng-containerize aplikasi backend FastAPI.
        *   File terkait: `backend/Dockerfile`
    *   **9.2**: Buat `Dockerfile` untuk meng-containerize aplikasi frontend React (misalnya, build statis yang di-serve oleh Nginx atau server statis lainnya).
        *   File terkait: `frontend/Dockerfile`
    *   **9.3**: Buat file `docker-compose.yml` untuk memudahkan menjalankan semua service (backend, frontend, database MySQL `sim_testgeluran`, Neo4j/Graphiti) secara lokal dalam container.
        *   File terkait: `docker-compose.yml`
    *   **9.4**: Tulis skrip atau instruksi untuk setup database dan Graphiti di dalam lingkungan Docker (misalnya, menggunakan skrip inisialisasi yang dijalankan saat container DB/Graphiti pertama kali start).
    *   **9.5**: **TESTING (STEP 9)**:
        *   Verifikasi aplikasi backend dan frontend bisa di-build menjadi image Docker.
        *   Verifikasi semua service bisa dijalankan bersamaan menggunakan `docker-compose up`.
        *   Lakukan tes fungsionalitas dasar pada aplikasi yang berjalan di Docker untuk memastikan semua koneksi antar service (Frontend -> Backend, Backend -> DB, Backend -> Neo4j, Backend -> LLM) berfungsi.

---
