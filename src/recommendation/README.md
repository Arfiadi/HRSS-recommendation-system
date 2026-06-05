# Recommendation Engine

Folder `src/recommendation/` memuat logika inti dari **Prescriptive Recommendation System**. Berbeda dengan sistem prediktif biasa yang hanya menebak klasifikasi data, sistem ini memberikan saran tindakan fisik secara langsung kepada operator pabrik.

## 🧠 Metodologi: Hybrid Intelligence

Sistem rekomendasi di proyek ini menggunakan arsitektur **Hybrid Intelligence** yang menggabungkan keunggulan *Data-Driven Machine Learning* dengan *Domain-Driven Expert Rules*.

### 1. Machine Learning Signal (Predictive)
Model Random Forest (atau algoritma lain) menelan raw data telemetri dan memprediksi "Apakah profil kelistrikan saat ini lebih mirip dengan mode Standard atau mode Optimized?". Outputnya berupa **probabilitas (0.0 - 1.0)**.

### 2. Rule Engine (Domain Knowledge)
Diimplementasikan pada `rule_engine.py`, komponen ini mengevaluasi konstrain fisika dan teknik mesin sesungguhnya dari alat HRSS. Aturan (rules) ini bertindak sebagai jaring pengaman (*safety net*) dari Machine Learning:
* **Rail Inefficiency**: Mendeteksi rasio pergerakan horizontal (Weg) yang tinggi namun dengan rasio efisiensi daya sangat rendah.
* **Overload / Friction Warning**: Mendeteksi tarikan arus listrik yang tinggi (A/W) namun pergerakan mekanis sangat minim (indikasi rel aus atau beban terlalu berat).
* **Voltage Sag Anomaly**: Mendeteksi *drop* tegangan berlebih pada *DC Bus* yang berbahaya untuk komponen elektronika.

### 3. Decision Policy (Prescriptive Arbiter)
Diimplementasikan pada `decision_policy.py`, komponen ini adalah pengambil keputusan final.
Metodologi:
- **Low Risk**: Model ML dan *current mode* selaras, serta TIDAK ADA peringatan dari *Rule Engine*. Tindakan: Pertahankan status quo.
- **Medium Inefficiency**: Model ML mendeteksi bahwa mode lain akan lebih hemat daya, dan TIDAK ADA peringatan *Rule Engine*. Tindakan: Sistem akan menyarankan transisi (Switch Mode) untuk menghemat biaya operasi.
- **High Inefficiency / Mechanical Anomaly**: *Rule Engine* mendeteksi anomali fisik. Terlepas dari apa probabilitas ML-nya, prioritas utama adalah keselamatan alat. Tindakan: Sistem merekomendasikan transisi paksa ke mode Standard (yang lebih pelan) dan menyarankan pengecekan perangkat keras (maintenance).

### 4. Scoring System
Diimplementasikan pada `scoring.py`. Mengkalkulasi *Efficiency Score* absolut dengan skala `0 - 100`. Metodologi kalkulasi:
* Basis skor (`Base Score`) = (Probabilitas Optimized dari ML) * 100.
* Penalti (`Penalty Deduction`) = Tiap *rule alert* yang terpicu akan memotong skor sebesar poin tertentu (misal: penalti 30% per alert).
* *Final Score* = `Base Score - Total Penalty` (Skor dibatasi agar tidak kurang dari 0).

Dengan metodologi *Hybrid* ini, sistem tidak hanya cerdas dalam mengenali pola data yang rumit, namun juga dijamin aman untuk diaplikasikan di dunia nyata berkat perlindungan logika *engineering* (*Domain Rules*).
