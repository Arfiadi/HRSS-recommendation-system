# BUSINESS UNDERSTANDING

## 1. Latar Belakang
Pada era industri modern, sistem otomatis seperti conveyor belt dan automated storage system digunakan untuk meningkatkan efisiensi proses produksi dan distribusi barang. Sistem tersebut bekerja secara kontinu untuk memindahkan package atau material antar lokasi menggunakan kombinasi conveyor dan rail movement.

Namun, peningkatan otomatisasi industri juga menyebabkan meningkatnya konsumsi energi operasional. Pola movement yang tidak efisien dapat menghasilkan konsumsi daya yang lebih tinggi, idle movement yang tidak diperlukan, serta operational cycle yang lebih lambat. Oleh karena itu, optimalisasi pola operasi menjadi salah satu tantangan penting dalam industrial energy management.

Dataset yang digunakan pada project ini berasal dari High Rack Storage System (HRSS) di Smart Factory Lemgo, Jerman. Sistem ini terdiri dari beberapa conveyor belt dan rail yang bekerja secara otomatis untuk memindahkan package antar posisi tertentu. Dataset merekam telemetry sensor berupa posisi movement, konsumsi daya listrik, tegangan, dan kondisi operasional sistem secara time-series.

Dalam dataset tersedia dua jenis operational scenario utama, yaitu:
- standard operation (non-optimized)
- optimized operation

Optimized operation menggunakan strategi simultaneous movement, yaitu conveyor middle dapat bergerak horizontal dan vertikal secara bersamaan untuk meningkatkan efisiensi operasional dan mengurangi konsumsi energi.

Berdasarkan kondisi tersebut, project ini bertujuan membangun sistem analitik dan rekomendasi operasional industri yang mampu:
- mengenali pola operasi efisien
- membedakan optimized dan non-optimized operation
- memberikan rekomendasi operational movement yang lebih hemat energi

## 2. Permasalahan Industri
Pada sistem conveyor dan rail otomatis, setiap movement menghasilkan konsumsi energi yang berbeda-beda tergantung pola operasi yang digunakan. Beberapa permasalahan utama pada sistem industri ini meliputi:
- Konsumsi energi yang tinggi pada operational movement tertentu.
- Sulitnya mengidentifikasi pola operasi yang paling efisien hanya dari pengamatan manual telemetry sensor.
- Tidak adanya sistem cerdas yang mampu memberikan rekomendasi operational strategy secara otomatis.
- Adanya perbedaan efisiensi antara standard operation dan optimized operation yang perlu dipelajari lebih lanjut secara data-driven.

Jika pola operasi yang tidak efisien terus digunakan, maka sistem dapat mengalami:
- pemborosan energi
- peningkatan operational cost
- penurunan efisiensi sistem otomatis
- penggunaan resource yang tidak optimal

## 3. Tujuan Project
Project ini bertujuan untuk membangun Industrial Operational Recommendation System berbasis telemetry sensor industri guna mendukung efisiensi energi operasional. Secara khusus, tujuan project meliputi:
- Menganalisis perbedaan operational behavior antara standard operation dan optimized operation.
- Mempelajari hubungan antara movement conveyor/rail dengan konsumsi energi sistem.
- Membangun model machine learning yang mampu mengenali pola operasi optimized dan non-optimized.
- Menghasilkan recommendation strategy untuk operational movement yang lebih efisien berdasarkan pola telemetry sensor.

## 4. Business Objective
Business objective dari project ini adalah meningkatkan efisiensi operasional sistem conveyor industri melalui pemanfaatan machine learning dan telemetry analytics. Target utama yang ingin dicapai antara lain:
- mengurangi konsumsi energi operasional
- meningkatkan efisiensi movement system
- membantu identifikasi operational pattern yang tidak efisien
- mendukung decision making berbasis data pada sistem industri otomatis

## 5. Success Criteria
Keberhasilan project dapat diukur melalui beberapa indikator berikut:

### 5.1 Machine Learning Success Criteria
- Model mampu membedakan optimized dan standard operation dengan performa klasifikasi yang baik.
- Model memiliki nilai Accuracy, Precision, Recall, dan F1-Score yang stabil.
- Model mampu mengenali pola operational behavior berdasarkan telemetry sensor.

### 5.2 Business Success Criteria
- Sistem mampu mengidentifikasi pola operasi dengan konsumsi energi tinggi.
- Sistem mampu memberikan recommendation strategy yang lebih efisien.
- Insight yang dihasilkan dapat membantu optimalisasi operational movement pada sistem industri.

---

# PROBLEM FRAMING

## 1. Definisi Masalah Machine Learning
Permasalahan utama pada project ini adalah bagaimana mengenali pola operasi industri yang efisien berdasarkan telemetry sensor dan menghasilkan rekomendasi operational movement yang lebih hemat energi. Masalah tersebut diformulasikan menjadi supervised machine learning problem dengan pendekatan binary classification.

## 2. Jenis Machine Learning Task
Jenis machine learning task pada project ini adalah **Binary Classification**. Model akan mempelajari pola telemetry sensor untuk membedakan:
- standard operation
- optimized operation

## 3. Target Variable
Target utama pada project ini adalah: `operation_type`
Dengan representasi class sebagai berikut:

| Class | Meaning |
|---|---|
| 0 | standard operation |
| 1 | optimized operation |

Kolom target dibentuk berdasarkan asal file dataset:
- `HRSS_normal_standard.csv` → class 0
- `HRSS_normal_optimized.csv` → class 1

## 4. Unit Analisis
Setiap baris data merepresentasikan snapshot kondisi sistem industri pada waktu tertentu. Setiap row berisi kondisi telemetry sensor seperti:
- posisi movement conveyor
- posisi rail
- konsumsi daya
- tegangan listrik
- kondisi operasional sistem

Dengan demikian, unit analisis pada project ini adalah **telemetry time-series operational snapshot**.

## 5. Input Features
Input model berasal dari telemetry sensor industri, meliputi:

**A. Movement / Position Features**
- *Contoh:* `I_w_BLO_Weg`, `I_w_BHL_Weg`, `I_w_BHR_Weg`, `I_w_HR_Weg`, `I_w_HL_Weg`
- *Fungsi:* merepresentasikan posisi movement conveyor dan rail.

**B. Power Features**
- *Contoh:* `O_w_BLO_power`, `O_w_BHR_power`, `O_w_HR_power`
- *Fungsi:* merepresentasikan konsumsi energi sistem.

**C. Voltage Features**
- *Contoh:* `O_w_BLO_voltage`, `O_w_HR_voltage`
- *Fungsi:* merepresentasikan kondisi dan kestabilan listrik sistem.

**D. Timestamp**
- *Fungsi:* merepresentasikan urutan waktu operasi sistem.

## 6. Output Sistem
Output utama sistem meliputi:

**A. Operational Prediction**
- Contoh: `optimized` atau `non-optimized`

**B. Recommendation Strategy**
Contoh recommendation:
- **Operational Status:** NON-OPTIMIZED
- **Recommendation:** 
  - → apply simultaneous movement
  - → reduce idle movement
  - → use optimized movement pattern
- **Expected Impact:**
  - → lower energy consumption
  - → improved operational efficiency

## 7. Recommendation System Perspective
Project ini bukan recommendation system tradisional seperti movie recommendation, product recommendation, atau collaborative filtering. Recommendation yang dihasilkan merupakan **Industrial Operational Recommendation** yang berfokus pada:
- operational strategy
- movement optimization
- energy efficiency improvement

Recommendation dihasilkan berdasarkan:
- classification result
- telemetry pattern
- energy behavior analysis
- operational efficiency insight

## 8. Scope Project
Scope utama project meliputi:
- telemetry analytics
- operational pattern recognition
- energy efficiency analysis
- classification-based recommendation system

Sedangkan anomaly detection tidak menjadi fokus utama project dan hanya digunakan sebagai kemungkinan pengembangan lanjutan di masa depan.
