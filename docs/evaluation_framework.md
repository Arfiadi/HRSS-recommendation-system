# Evaluation Framework

## Industrial Operational Recommendation System (HRSS)

---

# 1. Tujuan Evaluasi

Evaluasi dalam sistem ini tidak hanya bertujuan mengukur performa model machine learning, tetapi untuk menjawab pertanyaan utama:

> Seberapa baik sistem dapat mengambil keputusan operasional yang benar dalam konteks industri?

Dengan demikian, evaluasi tidak hanya berbasis akurasi, tetapi berbasis:

* kualitas keputusan
* risiko kesalahan operasional
* keseimbangan deteksi antar kelas

---

# 2. Karakteristik Masalah

Masalah ini adalah:

* Supervised Learning
* Binary Classification
* Imbalanced-aware (moderate imbalance)

Target:

```
operation_type
0 = standard operation
1 = optimized operation
```

Distribusi target:

* Standard: ~54.85%
* Optimized: ~45.15%

Implikasi:

> Tidak ekstrem imbalance, tetapi tetap membutuhkan evaluasi yang tidak bias terhadap kelas mayoritas.

---

# 3. Prinsip Evaluasi

Evaluasi sistem mengikuti prinsip:

## 3.1 Decision-Oriented Evaluation

Evaluasi harus mencerminkan kualitas keputusan operasional, bukan hanya performa statistik.

## 3.2 Class-Aware Evaluation

Setiap kelas memiliki dampak berbeda dalam konteks operasional.

## 3.3 Risk-Aware Evaluation

Kesalahan prediksi memiliki konsekuensi operasional yang berbeda.

---

# 4. Primary Metrics

## 4.1 F1-Score (Macro)

### Definisi

F1-macro adalah rata-rata F1-score dari setiap kelas tanpa memperhatikan distribusi kelas.

### Alasan penggunaan

* memastikan model tidak bias terhadap kelas mayoritas
* menjaga keseimbangan performa antar kelas
* penting untuk sistem keputusan dua kelas yang setara pentingnya

### Interpretasi dalam konteks sistem

Model harus mampu:

* mengenali standard operation dengan benar
* mengenali optimized operation dengan benar
  secara seimbang

---

## 4.2 ROC-AUC

### Definisi

Mengukur kemampuan model dalam membedakan dua kelas secara probabilistik.

### Alasan penggunaan

* tidak tergantung threshold
* mengukur kualitas ranking probabilitas
* penting untuk sistem rekomendasi berbasis probabilitas

### Interpretasi

Semakin tinggi ROC-AUC, semakin baik model dalam:

* membedakan operasi efisien vs tidak efisien

---

# 5. Secondary Metrics

## 5.1 Precision (Class 1 - Optimized)

Mengukur:

> dari semua prediksi optimized, berapa yang benar-benar optimized

### Relevansi

* penting untuk menghindari false optimism
* menjaga validitas rekomendasi efisiensi

---

## 5.2 Recall (Class 1 - Optimized)

Mengukur:

> dari semua optimized sebenarnya, berapa yang berhasil terdeteksi

### Relevansi

* penting untuk tidak melewatkan operasi efisien
* mendukung sistem optimasi operasional

---

# 6. Risk Metrics

## 6.1 False Negative Rate (FNR)

### Definisi

Kasus ketika:

* optimized operation diprediksi sebagai standard

### Dampak industri

* kehilangan peluang efisiensi
* sistem gagal mengidentifikasi operasi optimal

### Interpretasi

Semakin rendah FNR, semakin baik sistem dalam menangkap efisiensi.

---

## 6.2 False Positive Rate (FPR)

### Definisi

Kasus ketika:

* standard operation diprediksi sebagai optimized

### Dampak industri

* false assumption bahwa sistem sudah efisien
* keputusan optimasi yang salah

### Interpretasi

Semakin rendah FPR, semakin sedikit misleading insight.

---

# 7. Evaluation Strategy

## 7.1 Model Comparison Framework

Setiap model dievaluasi pada dua kondisi:

### A. Raw Features

* baseline representation
* tanpa feature engineering

### B. Engineered Features

* enhanced operational representation
* richer signal structure

Tujuan:

> mengukur dampak feature engineering terhadap kualitas keputusan

---

## 7.2 Evaluation Workflow

```
Train Model
    ↓
Predict Test Set
    ↓
Compute Metrics
    ↓
Compare Across Models
    ↓
Select Best Model
    ↓
Register in MLflow
```

---

# 8. Decision Interpretation Layer

Evaluasi tidak berhenti pada angka, tetapi diterjemahkan menjadi:

* tingkat efisiensi operasional
* risiko keputusan salah
* kualitas rekomendasi sistem

Contoh interpretasi:

* FNR tinggi → sistem melewatkan peluang optimasi
* FPR tinggi → sistem memberikan rekomendasi optimasi yang salah

---

# 9. Model Selection Criteria

Model terbaik tidak hanya dipilih berdasarkan akurasi, tetapi:

## Primary Priority

* F1-macro
* ROC-AUC

## Secondary Priority

* Recall class 1
* Precision class 1

## Risk Priority

* Minimalkan FNR
* Minimalkan FPR

---

# 10. Evaluation Philosophy

Evaluasi dalam sistem ini mengikuti prinsip:

> "A good model is not the most accurate model, but the most reliable decision-maker under operational constraints."

---

# 11. Summary

Framework evaluasi ini dirancang untuk memastikan bahwa sistem:

* tidak hanya akurat secara statistik
* tetapi juga robust secara keputusan operasional
* serta dapat diinterpretasikan dalam konteks industri nyata

Dengan demikian, evaluasi menjadi bagian dari **decision system**, bukan hanya model scoring.
