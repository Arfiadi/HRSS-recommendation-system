# Recommendation Engine

Folder `src/recommendation/` memuat logika inti dari **Prescriptive Recommendation System**. Berbeda dengan sistem prediktif biasa yang hanya menebak klasifikasi data, sistem ini memberikan saran tindakan operasional secara langsung (preskriptif) kepada operator pabrik (atau WMS).

## 🧠 Metodologi: Neuro-Symbolic / Hybrid AI

Sistem rekomendasi di proyek ini menggunakan arsitektur **Hybrid Intelligence** yang menggabungkan keunggulan *Data-Driven Machine Learning* sebagai pengenal pola, dengan *Domain-Driven Expert Rules* sebagai batasan keamanan fisik.

### 1. Machine Learning Signal (Strategist)
Model *Random Forest* membaca 18 fitur sensor *telemetry* dan memprediksi: "Apakah pola pergerakan saat ini beroperasi dengan rute *Standard* yang boros, atau rute *Optimized* yang hemat?". Outputnya berupa **probabilitas (0.0 - 1.0)** menuju *Optimized*.

### 2. Rule Engine (Safety Override)
Diimplementasikan pada `rule_engine.py`. Berbeda dengan ML yang murni berbasis data, *Rule Engine* dibangun berdasarkan batas fisika empiris dari motor HRSS. Aturan ini mengevaluasi batas keselamatan *hardware*:
* **Extreme Power Load**: Mendeteksi jika total konsumsi daya melonjak di atas batas kritis (P97 / >75.000 Watt), menandakan mesin sedang ditarik secara ekstrem melampaui batas aman.
* **Voltage Sag Under Load**: Mendeteksi jika motor rel utama (HL/HR) menarik daya beban berat (>5.000W) NAMUN tegangannya anjlok (Drop Voltage <20V), menandakan ketidakstabilan kelistrikan yang bisa merusak motor.

### 3. Decision Policy (Prescriptive Arbiter)
Diimplementasikan pada `decision_policy.py`. Komponen ini bertindak sebagai pengambil keputusan final yang merekomendasikan transisi mode pada WMS.
Logikanya dievaluasi melalui matriks berikut:
* **Jika tidak ada bahaya kelistrikan (Rules = Aman):**
  * *Aktual Standard, ML Standard*: Sistem menyarankan beralih ke *Optimized* untuk efisiensi.
  * *Aktual Standard, ML Optimized*: Sistem memuji rute yang tak sengaja efisien dan menyarankan transisi penuh.
  * *Aktual Optimized, ML Standard*: Sistem menegur bahwa algoritma rute *Optimized* saat ini sedang gagal / beroperasi layaknya rute *Standard* yang boros.
  * *Aktual Optimized, ML Optimized*: Sistem merekomendasikan untuk mempertahankan mode *Optimized*.
* **Jika ada bahaya kelistrikan (Rules = Bahaya):**
  * Terlepas dari tingkat efisiensi rute, sistem memprioritaskan keamanan alat. Sistem akan langsung menginstruksikan mesin untuk membuang mode *Smart Routing* dan kembali ke mode *Standard* (atau mengurangi beban) untuk menstabilkan kelistrikan *hardware*.

### 4. OEE-style Scoring System
Diimplementasikan pada `scoring.py`. Mengkalkulasi *System Energy Efficiency* (mirip *Overall Equipment Effectiveness*) dengan skala `0 - 100`.
Metodologi kalkulasi:
* **Base Score**: 100% (Diasumsikan mesin secara fisik sempurna).
* **Routing Penalty**: Potongan hingga 20 poin dari ML jika rute pergerakan terdeteksi tidak efisien (mendekati probabilitas *Standard*).
* **Physical Penalty**: Potongan dari *Rule Engine* jika terjadi anomali kelistrikan nyata (-15 poin untuk *Extreme Power*, -25 poin untuk *Voltage Sag*).
* *Final Score* = `100 - Routing Penalty - Physical Penalty` (Dibatasi di rentang 0-100).

Dengan metodologi *Hybrid* ini, sistem tidak hanya cerdas dalam mengenali pola data yang rumit, namun juga dijamin logis, aman, dan dapat dipertanggungjawabkan di industri berkat perlindungan logika teknik fisika (*Domain Rules*).
