Baik, kita akan membuat **Dokumen Inisialisasi Data dan Skema (untuk MVP)**.

Dokumen ini akan merinci bagaimana data sampel dan skema akan disiapkan dan dimuat untuk keperluan development dan testing MVP, baik untuk SQLite in-memory maupun Graphiti.

---

**Dokumen Perencanaan Tambahan 7: Inisialisasi Data dan Skema (untuk MVP)**

**Versi Dokumen**: 1.0
**Tanggal**: 23 Oktober 2024

**Daftar Isi**:
1.  Pendahuluan
2.  Sumber Data Sampel
    2.1. File `schema.sql` (Definisi Tabel)
    2.2. File `data.sql` (Data Sampel)
3.  Proses Inisialisasi Database SQLite In-Memory
4.  Proses Inisialisasi Graphiti Knowledge Graph
    4.1. Ekstraksi Skema dari `schema.sql`
    4.2. Penambahan Metadata Semantik
    4.3. Representasi Skema di Graphiti
5.  Skrip Inisialisasi (Konsep)
6.  Contoh Data dan Skema yang Diinisialisasi

---

**1. Pendahuluan**

Untuk pengembangan dan pengujian MVP AI Agent yang efektif, diperlukan satu set data dan skema yang konsisten dan representatif. Dokumen ini menjelaskan proses untuk menginisialisasi database sampel (SQLite in-memory) dan Graphiti Knowledge Graph. Proses ini memastikan bahwa setiap developer dan setiap siklus pengujian dimulai dengan dasar data yang sama.

---

**2. Sumber Data Sampel**

Data sampel dan definisi skema akan disimpan dalam dua file SQL terpisah:

**2.1. File `schema.sql` (Definisi Tabel)**
File ini akan berisi pernyataan `CREATE TABLE` untuk semua tabel yang relevan dengan skenario MVP.
*   **Tujuan**: Mendefinisikan struktur database.
*   **Contoh Isi `schema.sql`**:
    ```sql
    -- Tabel untuk mencatat order penjualan
    CREATE TABLE sales_orders (
        order_id VARCHAR(50) PRIMARY KEY,
        order_date DATE NOT NULL,
        customer_id VARCHAR(50) NOT NULL,
        total_amount DECIMAL(18, 2) NOT NULL,
        status VARCHAR(20) DEFAULT 'COMPLETED' -- e.g., COMPLETED, PENDING, CANCELLED
        -- FOREIGN KEY (customer_id) REFERENCES customers(customer_id) -- Jika tabel customers ada
    );

    -- Tabel untuk detail item per order
    CREATE TABLE order_lines (
        line_id VARCHAR(50) PRIMARY KEY,
        order_id VARCHAR(50) NOT NULL,
        product_id VARCHAR(50) NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price DECIMAL(10, 2) NOT NULL,
        sub_total_amount DECIMAL(18, 2) NOT NULL, -- quantity * unit_price
        FOREIGN KEY (order_id) REFERENCES sales_orders(order_id)
        -- FOREIGN KEY (product_id) REFERENCES products(product_id) -- Jika tabel products ada
    );

    -- Tabel untuk data pelanggan (opsional untuk MVP awal jika fokus hanya pada sales)
    CREATE TABLE customers (
        customer_id VARCHAR(50) PRIMARY KEY,
        customer_name VARCHAR(255) NOT NULL,
        segment VARCHAR(50) -- e.g., RETAIL, CORPORATE
    );

    -- Tabel untuk data produk (opsional untuk MVP awal)
    CREATE TABLE products (
        product_id VARCHAR(50) PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        category VARCHAR(100) -- e.g., ELECTRONICS, FASHION
    );

    -- Tabel untuk data karyawan (opsional untuk MVP awal)
    CREATE TABLE employees (
        employee_id VARCHAR(50) PRIMARY KEY,
        employee_name VARCHAR(255) NOT NULL,
        department VARCHAR(100),
        hire_date DATE
    );
    ```
    *(Tambahkan tabel lain sesuai kebutuhan skenario MVP, misalnya `employees` jika ada query terkait data karyawan, atau `customers` jika ada query terkait laporan pelanggan)*

**2.2. File `data.sql` (Data Sampel)**
File ini akan berisi pernyataan `INSERT INTO` untuk mengisi tabel-tabel yang telah dibuat dengan data sampel.
*   **Tujuan**: Menyediakan data konkret untuk di-query dan dianalisis.
*   **Contoh Isi `data.sql`**:
    ```sql
    -- Data untuk sales_orders
    INSERT INTO sales_orders (order_id, order_date, customer_id, total_amount, status) VALUES
    ('ORD-001', '2023-01-15', 'CUST-123', 150000.00, 'COMPLETED'),
    ('ORD-002', '2023-01-20', 'CUST-456', 275000.50, 'COMPLETED'),
    ('ORD-003', '2023-02-10', 'CUST-123', 80000.00, 'PENDING'),
    ('ORD-004', '2023-01-28', 'CUST-789', 120000.75, 'COMPLETED');

    -- Data untuk order_lines
    INSERT INTO order_lines (line_id, order_id, product_id, quantity, unit_price, sub_total_amount) VALUES
    ('LINE-001A', 'ORD-001', 'PROD-A', 2, 50000.00, 100000.00),
    ('LINE-001B', 'ORD-001', 'PROD-B', 1, 50000.00, 50000.00),
    ('LINE-002A', 'ORD-002', 'PROD-C', 5, 55000.10, 275000.50),
    ('LINE-003A', 'ORD-003', 'PROD-A', 1, 80000.00, 80000.00),
    ('LINE-004A', 'ORD-004', 'PROD-D', 3, 40000.25, 120000.75);

    -- Data untuk customers (jika ada)
    INSERT INTO customers (customer_id, customer_name, segment) VALUES
    ('CUST-123', 'PT ABC Corp', 'CORPORATE'),
    ('CUST-456', 'CV XYZ Trading', 'RETAIL'),
    ('CUST-789', 'Toko Maju Jaya', 'RETAIL');

    -- Data untuk products (jika ada)
    INSERT INTO products (product_id, product_name, category) VALUES
    ('PROD-A', 'Laptop Stand', 'Aksesoris Komputer'),
    ('PROD-B', 'Mouse Wireless', 'Aksesoris Komputer'),
    ('PROD-C', 'Keyboard Mekanik', 'Aksesoris Komputer'),
    ('PROD-D', 'Webcam HD', 'Periferal');
    ```
    *(Data sampel harus cukup beragam untuk menguji berbagai skenario query, termasuk filter tanggal, agregasi, dan join jika ada).*

---

**3. Proses Inisialisasi Database SQLite In-Memory**

Saat aplikasi AI Agent (atau sesi testing) dimulai, proses berikut akan terjadi:
1.  Buat koneksi ke database SQLite in-memory.
2.  Baca file `schema.sql`.
3.  Eksekusi setiap pernyataan `CREATE TABLE` dari `schema.sql` pada koneksi SQLite.
4.  Baca file `data.sql`.
5.  Eksekusi setiap pernyataan `INSERT INTO` dari `data.sql` pada koneksi SQLite.
6.  Koneksi database SQLite yang sudah terisi ini kemudian akan digunakan oleh `mysql_mcp_server`.

---

**4. Proses Inisialisasi Graphiti Knowledge Graph**

Graphiti perlu diisi dengan metadata skema yang diperkaya. Ini bisa dilakukan saat aplikasi pertama kali dijalankan atau sebagai langkah pra-pemrosesan.

**4.1. Ekstraksi Skema dari `schema.sql` (Otomatis atau Semi-Otomatis)**
*   Sebuah skrip atau parser sederhana akan membaca file `schema.sql`.
*   Parser ini akan mengidentifikasi:
    *   Nama-nama tabel.
    *   Nama-nama kolom per tabel beserta tipe datanya (misalnya, `VARCHAR`, `DATE`, `DECIMAL`).
    *   Informasi *primary key* dan *foreign key* (jika didefinisikan secara eksplisit).

**4.2. Penambahan Metadata Semantik (Manual atau Terpandu)**
Setelah struktur dasar diekstrak, metadata semantik perlu ditambahkan. Untuk MVP, ini bisa dilakukan secara manual melalui skrip atau konfigurasi file.
*   **Untuk setiap Tabel**:
    *   `purpose`: Deskripsi singkat tujuan tabel (misalnya, "Mencatat transaksi penjualan harian").
    *   `business_category`: Kategori bisnis (misalnya, "financial", "operational", "master_data").
*   **Untuk setiap Kolom**:
    *   `description`: Deskripsi fungsional kolom (misalnya, "Tanggal order dibuat oleh pelanggan").
    *   `classification`: Klasifikasi kolom (misalnya, `financial_amount`, `temporal`, `identifier`, `descriptive`, `quantitative`).
    *   `is_aggregatable`: Boolean, apakah kolom ini umumnya diagregasi (misalnya, `total_amount` bisa di-`SUM`, `product_name` tidak).
    *   Contoh nilai (jika relevan dan membantu LLM).

**4.3. Representasi Skema di Graphiti**
Data skema yang telah diperkaya ini akan direpresentasikan sebagai *nodes* dan *edges* di Graphiti.
*   **Nodes**:
    *   `TableNode`: Mewakili setiap tabel. Atribut: `name`, `purpose`, `business_category`.
    *   `ColumnNode`: Mewakili setiap kolom. Atribut: `name`, `type`, `description`, `classification`, `is_aggregatable`.
*   **Edges**:
    *   `HAS_COLUMN`: Dari `TableNode` ke `ColumnNode`.
    *   `RELATIONSHIP` (atau `FOREIGN_KEY_TO`): Dari `ColumnNode` (foreign key) ke `ColumnNode` (primary key di tabel lain). Atribut: `type` (misal, `1-to-N`).

**Contoh Metadata Semantik Tambahan untuk `sales_orders`**:
*   Tabel `sales_orders`:
    *   `purpose`: "Mencatat semua transaksi penjualan yang telah terjadi."
    *   `business_category`: "financial_transaction"
*   Kolom `order_date` di `sales_orders`:
    *   `description`: "Tanggal ketika order penjualan dibuat."
    *   `classification`: "temporal"
    *   `is_aggregatable`: `false` (umumnya untuk filtering, bukan agregasi langsung seperti SUM)
*   Kolom `total_amount` di `sales_orders`:
    *   `description`: "Total nilai moneter dari order penjualan setelah diskon dan pajak."
    *   `classification`: "financial_amount"
    *   `is_aggregatable`: `true`

---

**5. Skrip Inisialisasi (Konsep)**

Sebuah skrip Python (misalnya, `initialize_mvp_data.py`) akan dibuat untuk mengotomatiskan proses di atas:
*   Fungsi untuk membuat dan mengisi SQLite in-memory dari `schema.sql` dan `data.sql`.
*   Fungsi untuk mem-parse `schema.sql` (langkah 4.1).
*   Fungsi untuk membaca konfigurasi metadata semantik tambahan (misalnya, dari file JSON/YAML).
*   Fungsi untuk mempopulasi Graphiti dengan nodes dan edges skema yang telah diperkaya (langkah 4.3). Ini akan melibatkan interaksi dengan Graphiti, mungkin melalui Graphiti Python client atau API-nya jika tersedia, atau melalui `graphiti_mcp_server` jika sudah ada *tool* untuk menambahkan/mengupdate skema. Untuk MVP, cara termudah mungkin dengan skrip Python yang langsung menggunakan library Graphiti.

Skrip ini bisa dijalankan:
*   Setiap kali server FastAPI dimulai (untuk mode development).
*   Sebagai bagian dari setup lingkungan testing.

---

**6. Contoh Data dan Skema yang Diinisialisasi**

**6.1. SQLite In-Memory akan berisi**:
*   Tabel `sales_orders` dengan 4 baris data.
*   Tabel `order_lines` dengan 4 baris data.
*   Tabel `customers` dengan 3 baris data.
*   Tabel `products` dengan 4 baris data.

**6.2. Graphiti Knowledge Graph akan berisi (minimal)**:
*   `TableNode` untuk `sales_orders`, `order_lines`, `customers`, `products`.
*   `ColumnNode` untuk setiap kolom dalam tabel-tabel tersebut, lengkap dengan metadata semantik (tipe, deskripsi, klasifikasi, dll.).
*   `Edge` yang merepresentasikan relasi `FOREIGN KEY` antara `order_lines.order_id` dan `sales_orders.order_id`.
*   (Jika ada) `Edge` lain untuk relasi ke `customers` dan `products`.

---
