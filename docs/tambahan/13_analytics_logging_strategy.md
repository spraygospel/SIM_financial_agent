
### **Dokumen Teknis: 13_analytics_logging_strategy.md**

**Versi Dokumen**: 1.0
**Tanggal**: (Tanggal saat ini)

---

## **Bab 1: Pendahuluan dan Tujuan Logging**

### **1.1. Latar Belakang**

Pengembangan sebuah AI Agent yang andal tidak berhenti setelah fungsionalitasnya berjalan. Untuk memastikan agent ini memberikan nilai nyata, dapat diandalkan dalam jangka panjang, dan dapat terus berkembang, kita memerlukan cara untuk mengukur, memantau, dan memahami kinerjanya secara objektif.

Dokumen ini mendefinisikan strategi untuk **Logging Analitik Terstruktur**. Ini berbeda dari logging untuk debugging teknis; tujuannya bukan untuk melacak error baris per baris, melainkan untuk mengumpulkan data telemetri dari setiap interaksi pengguna. Data ini akan menjadi fondasi untuk pengambilan keputusan berbasis data di masa depan.

### **1.2. Tujuan Strategi Logging**

Implementasi logging analitik ini memiliki tiga tujuan utama yang saling terkait:

**1. Tujuan Bisnis: Membuktikan Nilai (Proving Value)**
*   **Pertanyaan yang Ingin Dijawab:** Seberapa sering agent digunakan? Berapa banyak query yang berhasil dijawab? Apakah penggunaan agent meningkat dari waktu ke waktu?
*   **Dampak:** Memberikan metrik kuantitatif yang dapat ditunjukkan kepada pemangku kepentingan dan investor untuk membuktikan Return on Investment (ROI) dari proyek ini (misalnya, "Agent berhasil menangani 1.000 permintaan data bulan ini, yang setara dengan estimasi X jam kerja analis").

**2. Tujuan Produk: Menginformasikan Pengembangan (Informing Development)**
*   **Pertanyaan yang Ingin Dijawab:** Fitur atau intent mana yang paling sering digunakan? Di bagian mana pengguna paling sering mengalami kegagalan? Jenis query apa yang belum bisa ditangani oleh agent?
*   **Dampak:** Data ini akan menjadi panduan untuk prioritas pengembangan di masa depan. Jika data menunjukkan banyak permintaan modifikasi (`REQUEST_MODIFICATION`) yang gagal, kita tahu area itu perlu perbaikan. Jika banyak query tentang perbandingan, kita tahu fitur `SYNTHESIZE_HISTORY` harus menjadi prioritas berikutnya.

**3. Tujuan Teknis: Memantau Kesehatan Sistem (Monitoring Health)**
*   **Pertanyaan yang Ingin Dijawab:** Berapa waktu respons rata-rata? Apakah ada node tertentu dalam alur kerja yang menjadi *bottleneck* (lambat)? Apakah ada peningkatan jumlah error setelah pembaruan?
*   **Dampak:** Memungkinkan kita untuk secara proaktif mengidentifikasi masalah performa, mengoptimalkan alur kerja, dan memastikan agent tetap responsif dan andal seiring waktu.

---

## **Bab 2: Struktur Log Analitik (`AnalyticsLogEntry`)**

### **2.1. Desain "Kontrak Data" Log**

Untuk memastikan data analitik kita konsisten dan mudah diolah, setiap interaksi yang selesai (baik sukses maupun gagal) akan menghasilkan satu entri log dengan struktur yang terdefinisi dengan baik. Struktur ini akan kita definisikan sebagai `TypedDict` atau Pydantic Model bernama `AnalyticsLogEntry`.

Berikut adalah definisi rinci untuk setiap field dalam `AnalyticsLogEntry`.

### **2.2. Definisi Field `AnalyticsLogEntry`**

```typescript
// Direpresentasikan dalam format mirip TypeScript untuk kejelasan
interface AnalyticsLogEntry {
  // === Informasi Identifikasi ===
  log_id: string; // UUID unik untuk setiap entri log.
  session_id: string; // ID sesi percakapan, untuk mengelompokkan interaksi.
  event_timestamp: string; // Timestamp saat log dibuat (akhir interaksi), format ISO 8601 UTC.

  // === Informasi Permintaan Pengguna ===
  user_query_text: string; // Teks asli dari query pengguna.
  detected_intent: string; // Intent yang terdeteksi oleh Router (e.g., 'EXECUTE_QUERY', 'ACKNOWLEDGE_RESPONSE').

  // === Metrik Status & Kualitas ===
  workflow_status: 'completed' | 'error'; // Status akhir dari alur kerja.
  final_quality_score?: number; // Skor kualitas data dari 0-100 (jika alur query sukses).
  analysis_confidence_score?: number; // Skor kepercayaan analisis dari 0-100 (jika alur query sukses).
  was_fallback_used: boolean; // Apakah agent menggunakan mekanisme fallback?
  was_repair_loop_used: boolean; // Apakah 'Validation & Repair Loop' terpicu?

  // === Metrik Performa (dalam milidetik) ===
  total_duration_ms: number; // Total waktu dari awal hingga akhir interaksi.
  router_duration_ms?: number; // Waktu yang dihabiskan di node Router.
  planning_duration_ms?: number; // Waktu untuk plan_execution (+ repair loop jika ada).
  mcp_calls_duration_ms?: number; // Total waktu gabungan untuk semua panggilan ke MCP Server.
  validation_duration_ms?: number; // Waktu untuk validasi rencana dan hasil.

  // === Konteks Eksekusi (jika relevan) ===
  tables_used?: string[]; // Daftar tabel utama yang digunakan (dari data_source_info).
  num_db_operations?: number; // Jumlah operasi dalam DatabaseOperationPlan.

  // === Informasi Error (jika workflow_status == 'error') ===
  error_source_node?: string; // Nama node LangGraph tempat error kritis terjadi.
  error_details?: string; // Pesan teknis dari error.
}
```

Struktur yang kaya ini akan memberi kita kemampuan untuk menjawab hampir semua pertanyaan bisnis, produk, dan teknis tentang kinerja AI Agent kita.


---

### **Dokumen Teknis: 13_analytics_logging_strategy.md**

---

## **Bab 3: Implementasi dalam Alur Kerja LangGraph**

### **3.1. Peran `log_analytics_node`**

Untuk memastikan pencatatan analitik dilakukan secara konsisten dan andal, kita akan mengimplementasikan sebuah node khusus bernama **`log_analytics_node`**. Node ini memiliki peran dan karakteristik sebagai berikut:

*   **Titik Keluar Tunggal (Single Exit Point):** Semua cabang alur kerja LangGraph, baik yang berakhir dengan sukses (`replace_placeholders`, `generate_acknowledgement`) maupun yang berakhir dengan kegagalan (`generate_error_response`), akan diarahkan ke `log_analytics_node` sebelum benar-benar berakhir (`END`). Ini menjamin bahwa **setiap interaksi akan tercatat**, tanpa terkecuali.
*   **Operasi "Baca-Saja" (Read-Only Operation):** Node ini tidak mengubah `AgentState` yang akan dikembalikan kepada pengguna. Tugasnya hanya membaca `AgentState` akhir, mengumpulkan metrik, dan mengirimkannya ke sistem penyimpanan log.
*   **Proses Asinkron (Fire-and-Forget):** Proses penulisan log harus dirancang agar tidak memblokir atau memperlambat pengembalian respons ke pengguna. Operasi I/O (penulisan ke file atau pengiriman ke layanan eksternal) idealnya dijalankan secara asinkron.

### **3.2. Pengumpulan Metrik Selama Alur Berlangsung**

Agar `log_analytics_node` memiliki data yang kaya untuk dicatat, metrik-metrik performa perlu dikumpulkan selama alur kerja berlangsung dan ditambahkan ke `AgentState`.

*   **Pengukuran Durasi:** Setiap node utama (misalnya, `router_node`, `plan_execution_node`, `execute_query_node`) akan bertanggung jawab untuk mengukur durasi eksekusinya sendiri.
    *   **Mekanisme:** Di awal setiap node, catat `start_time`. Di akhir, hitung `duration = datetime.now() - start_time`. Durasi ini kemudian ditambahkan ke sebuah `dict` khusus di dalam `AgentState`, misalnya `state['performance_trace']['plan_execution_ms'] = duration.total_seconds() * 1000`.
*   **Pencatatan Status Penting:**
    *   Node `validate_plan_node` akan menyetel `state['was_repair_loop_used'] = True` jika "repair loop" terpicu.
    *   Node-node yang menangani *fallback* (jika ada di masa depan) akan menyetel `state['was_fallback_used'] = True`.

### **3.3. Logika di dalam `log_analytics_node`**

Berikut adalah pseudocode yang menggambarkan apa yang akan terjadi di dalam `log_analytics_node`:

```python
def log_analytics_node(state: AgentState):
    # 1. Inisialisasi entri log dengan data dasar
    log_entry = AnalyticsLogEntry(
        log_id=str(uuid.uuid4()),
        session_id=state.get("session_id"),
        event_timestamp=datetime.utcnow().isoformat() + "Z",
        user_query_text=state.get("user_query"),
        detected_intent=state.get("detected_intent"),
        workflow_status=state.get("workflow_status")
    )

    # 2. Ambil metrik performa dari performance_trace
    perf_trace = state.get("performance_trace", {})
    log_entry["total_duration_ms"] = perf_trace.get("total_duration_ms")
    # ... isi semua metrik durasi lainnya ...

    # 3. Ambil metrik kualitas dan status
    if state.get("workflow_status") == "completed":
        log_entry["final_quality_score"] = state.get("quality_score")
        log_entry["analysis_confidence_score"] = state.get("analysis_confidence", {}).get("score")
        log_entry["tables_used"] = state.get("data_source_info", {}).get("tables_used", [])
    else: # Jika error
        log_entry["error_source_node"] = state.get("current_node_name") # Node terakhir sebelum error
        log_entry["error_details"] = state.get("technical_error_details")

    # 4. Kirim log ke sistem penyimpanan
    save_log_entry_to_storage(log_entry)

    # 5. Kembalikan state apa adanya tanpa modifikasi
    return state
```

---

## **Bab 4: Penyimpanan dan Analisis (Strategi MVP)**

### **4.1. Strategi Penyimpanan untuk MVP**

Untuk menjaga agar MVP tetap ramping dan cepat dikembangkan, kita akan menggunakan strategi penyimpanan log yang paling sederhana namun efektif: **penulisan ke file lokal dalam format JSON Lines.**

*   **Format:** JSON Lines (atau `ndjson`) adalah format di mana setiap baris dalam file teks adalah objek JSON yang valid. Ini sangat efisien untuk dibaca dan di-parse oleh banyak sistem analitik.
*   **Lokasi File:** `logs/analytics.log`. Direktori `logs` akan berada di root proyek backend dan harus dikecualikan dari Git.
*   **Rotasi Log:** Untuk mencegah file log menjadi terlalu besar, kita dapat mengimplementasikan mekanisme rotasi log sederhana (misalnya, membuat file baru setiap hari seperti `analytics-YYYY-MM-DD.log`).
*   **Keuntungan:**
    *   **Implementasi Cepat:** Tidak memerlukan setup infrastruktur eksternal.
    *   **Mudah Dianalisis:** File ini dapat dengan mudah diimpor ke Pandas, Elasticsearch, atau dibaca baris per baris oleh skrip kustom.
    *   ***Future-Proof*:** Aliran log ini dapat dengan mudah diarahkan ke layanan terpusat (seperti Fluentd atau Logstash) di masa depan.

### **4.2. Contoh Analisis Sederhana (Menggunakan Skrip)**

Setelah data terkumpul di `analytics.log`, kita dapat membuat skrip Python sederhana (`scripts/analyze_logs.py`) untuk menjawab pertanyaan-pertanyaan kunci.

**Contoh Pseudocode Skrip Analisis:**
```python
import pandas as pd
import json

def analyze_agent_logs(log_file_path="logs/analytics.log"):
    # Baca file log JSON Lines ke dalam DataFrame Pandas
    data = [json.loads(line) for line in open(log_file_path)]
    df = pd.DataFrame(data)
    
    # 1. Hitung total interaksi
    total_interactions = len(df)
    print(f"Total Interaksi: {total_interactions}")

    # 2. Analisis Tingkat Keberhasilan
    success_rate = df["workflow_status"].value_counts(normalize=True).get("completed", 0) * 100
    print(f"Tingkat Keberhasilan: {success_rate:.2f}%")

    # 3. Analisis Distribusi Intent
    print("\nDistribusi Intent:")
    print(df["detected_intent"].value_counts())

    # 4. Analisis Performa Rata-rata
    avg_duration = df[df["workflow_status"] == "completed"]["total_duration_ms"].mean()
    print(f"\nRata-rata Waktu Respons (Sukses): {avg_duration:.0f} ms")

    # 5. Identifikasi Error Paling Umum
    print("\nNode Penyebab Error Teratas:")
    print(df.dropna(subset=["error_source_node"])["error_source_node"].value_counts())

# Jalankan analisis
analyze_agent_logs()
```

### **4.3. Visi Jangka Panjang**

Strategi file log ini adalah fondasi yang sempurna. Seiring dengan pertumbuhan produk, kita dapat dengan mudah mengembangkan sistem ini:
1.  **Visualisasi:** Menggunakan **Elasticsearch + Kibana** atau **Grafana** untuk membuat dasbor real-time dari data di `analytics.log`.
2.  **Peringatan (Alerting):** Menyiapkan peringatan otomatis jika tingkat error (`workflow_status == 'error'`) tiba-tiba melonjak atau jika waktu respons rata-rata (`total_duration_ms`) meningkat secara signifikan.
3.  **Analisis Perilaku Pengguna:** Menganalisis `session_id` untuk memahami bagaimana pengguna berinteraksi dalam satu sesi, query apa yang mereka ajukan secara berurutan, dan di mana mereka berhenti.

Dengan pendekatan ini, kita tidak hanya membangun agent, tetapi juga membangun "sistem saraf" untuk memantau dan memahaminya.