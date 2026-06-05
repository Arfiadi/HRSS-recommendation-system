# Recommendation Engine

Folder `src/recommendation/` memuat logika inti dari **Prescriptive Recommendation System**. Berbeda dengan sistem prediktif biasa yang hanya menebak klasifikasi data, sistem ini memberikan saran tindakan fisik secara langsung kepada operator pabrik.

## 🧠 Metodologi: Hybrid Intelligence

Sistem rekomendasi di proyek ini menggunakan arsitektur **Hybrid Intelligence** yang menggabungkan keunggulan *Data-Driven Machine Learning* dengan *Domain-Driven Expert Rules*.

### 1. Machine Learning Signal (Predictive)
Model Random Forest (atau algoritma lain) menelan raw data telemetri dan memprediksi "Apakah profil kelistrikan saat ini lebih mirip dengan mode Standard atau mode Optimized?". Outputnya berupa **probabilitas (0.0 - 1.0)**.

### 2. Rule Engine (Domain Knowledge)
Diimplementasikan pada `rule_engine.py`, komponen ini mengevaluasi telemetri kelistrikan dan mekanis alat HRSS berdasarkan konstrain operasional:
* **Rail Inefficiency**: Mendeteksi aktivitas pergerakan horizontal yang tinggi namun dengan rasio efisiensi daya yang sangat rendah, menyarankan optimasi *routing* pada WMS.
* **Inefficient High Power**: Mendeteksi tarikan daya listrik yang tinggi dengan pergerakan mekanis yang sangat minim, mengindikasikan pemborosan daya akibat pergerakan *idle*.
* **Electrical Power Instability**: Mendeteksi penurunan tegangan rata-rata operasional yang menandakan bahwa pergerakan serentak (*simultaneous*) menjadi kurang efisien secara kelistrikan.

### 3. Decision Policy (Prescriptive Arbiter)
Diimplementasikan pada `decision_policy.py`, komponen ini bertindak sebagai pengambil keputusan final (rekomendasi preskriptif).
Metodologi:
- **Low Risk**: Model ML dan mode operasional saat ini selaras, serta TIDAK ADA peringatan dari *Rule Engine*. Tindakan: Pertahankan pola operasi saat ini (*Maintain current pattern*).
- **Medium Inefficiency**: Model ML memprediksi profil optimasi yang berbeda dengan mode operasional saat ini, namun TIDAK ADA hambatan operasional dari *Rule Engine*. Tindakan: Sistem menyarankan penyesuaian strategi (*Switch Mode*) untuk meningkatkan efisiensi energi.
- **High Inefficiency / Operational Deviation**: *Rule Engine* mendeteksi pelanggaran efisiensi daya atau instabilitas kelistrikan. Terlepas dari prediksi ML, sistem memprioritaskan mitigasi pemborosan energi. Tindakan: Merekomendasikan transisi profil paksa ke mode Standard untuk menstabilkan konsumsi daya alat.

### 4. Scoring System
Diimplementasikan pada `scoring.py`. Mengkalkulasi *Efficiency Score* absolut dengan skala `0 - 100`. Metodologi kalkulasi:
* Basis skor (`Base Score`) = (Probabilitas Optimized dari ML) * 100.
* Penalti (`Penalty Deduction`) = Tiap *rule alert* yang terpicu akan memotong skor sebesar poin tertentu (misal: penalti 30% per alert).
* *Final Score* = `Base Score - Total Penalty` (Skor dibatasi agar tidak kurang dari 0).

Dengan metodologi *Hybrid* ini, sistem tidak hanya cerdas dalam mengenali pola data yang rumit, namun juga dijamin aman untuk diaplikasikan di dunia nyata berkat perlindungan logika *engineering* (*Domain Rules*).
