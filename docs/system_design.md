# System Design

## Industrial Operational Recommendation System (HRSS)

---

# 1. Tujuan Sistem

Sistem ini dirancang untuk membangun **decision support system berbasis machine learning** yang mampu:

* Mengklasifikasikan jenis operasi HRSS (standard vs optimized)
* Menganalisis hubungan antara aktivitas movement dan konsumsi energi
* Menghasilkan rekomendasi peningkatan efisiensi operasional
* Menyediakan pipeline eksperimen yang dapat direproduksi

Fokus utama sistem bukan hanya prediksi, tetapi **pengambilan keputusan berbasis data industri**.

---

# 2. Konsep Sistem (System Thinking)

Sistem ini terdiri dari 4 lapisan utama:

```
Data → Model → Service → Decision → Interface
```

Namun secara teknis dibagi menjadi beberapa modul agar scalable:

* Data Pipeline Layer
* Feature Engineering Layer
* ML Model Layer
* Inference Service Layer
* Recommendation Layer
* Observability Layer (MLflow)

---

# 3. Data Flow Design

## 3.1 Alur Data End-to-End

```
Raw HRSS Data
      ↓
Data Cleaning & Validation
      ↓
Feature Engineering
      ↓
Train/Test Split (Fixed)
      ↓
Model Training (PyCaret)
      ↓
Best Model Selection
      ↓
Model Registry (MLflow)
      ↓
Inference Service
      ↓
Recommendation Engine
      ↓
Output (Prediction + Insight)
```

---

## 3.2 Prinsip Data Flow

* Data split bersifat fixed (tidak diacak ulang di training)
* Raw dan engineered dataset dipisahkan
* Tidak ada data leakage antar tahap
* Semua eksperimen harus dapat direproduksi melalui MLflow

---

# 4. Model Design

## 4.1 Problem Type

* Supervised Learning
* Binary Classification

Target:

```
operation_type
0 = standard operation
1 = optimized operation
```

---

## 4.2 Model Candidates

* Logistic Regression (baseline interpretability)
* Decision Tree (rule-based insight)
* Random Forest (robust non-linear model)
* XGBoost (performance benchmark)

Model menyesuaikan berdasarkan hasil eksperimen pycaret
---

## 4.3 Model Selection Strategy

Model tidak dipilih hanya berdasarkan accuracy, tetapi:

Primary Metrics:

* F1-score (macro)
* ROC-AUC

Risk Metrics:

* False Negative Rate (FNR)
* False Positive Rate (FPR)

Secondary Metrics:

* Precision class 1
* Recall class 1

---

# 5. Inference System Design

## 5.1 Inference Flow

```
Input Data (sensor / feature vector)
        ↓
Preprocessing (standardized pipeline)
        ↓
Feature alignment
        ↓
Model loading (MLflow / model registry)
        ↓
Prediction output
        ↓
Post-processing
        ↓
Recommendation engine
```

---

## 5.2 Inference Service (Core Component)

Inference dilakukan melalui satu entry point:

```
inference_service.py
```

Fungsi utama:

* Menghindari logic tersebar di UI
* Menyatukan preprocessing + prediction
* Menyediakan output terstruktur

Output standar:

```json
{
  "prediction": 1,
  "probability": 0.87,
  "risk_level": "high",
  "recommendation": "Reduce rail activity"
}
```

---

# 6. MLflow Integration Design

## 6.1 Peran MLflow

MLflow digunakan untuk:

* Tracking eksperimen model
* Logging metrics
* Menyimpan model artifacts
* Membandingkan RAW vs ENGINEERED pipeline

---

## 6.2 Experiment Structure

Dua eksperimen utama:

### Experiment 1: RAW Features

* baseline model performance
* tanpa feature engineering

### Experiment 2: Engineered Features

* enriched operational signals
* improved representation learning

---

## 6.3 Model Lifecycle

```
Train → Log MLflow → Evaluate → Select Best → Register Model → Deploy
```

---

# 7. Recommendation System Design

## 7.1 Approach

Hybrid system:

* Rule-based logic (domain knowledge)
* Model-driven signals (probability output)

---

## 7.2 Rule Engine Example

```
IF rail_activity tinggi AND energy_usage tinggi THEN
    inefficiency = TRUE
    recommendation = "Optimize rail movement"
```

---

## 7.3 Decision Policy Layer

Layer ini bertugas:

* Menggabungkan hasil model + rule engine
* Menentukan tingkat risiko
* Menghasilkan rekomendasi final

Output kategori:

* Low risk operation
* Medium inefficiency
* High inefficiency

---

# 8. Interface Interaction Design

## 8.1 Streamlit Flow

User akan berinteraksi melalui:

* Overview system
* Prediction input
* Recommendation output
* Model comparison
* Explainability layer

---

## 8.2 UI tidak mengandung logic utama

Prinsip penting:

> UI hanya konsumsi service layer, tidak menjalankan ML logic

---

# 9. Scalability Design

## 9.1 Current State

* Batch inference
* Notebook-driven experimentation
* Streamlit as interface

---

## 9.2 Future State (Stage 2)

* FastAPI inference service
* Model registry abstraction
* Real-time prediction endpoint

---

## 9.3 Future State (Stage 3)

* Streaming telemetry ingestion
* Feature store
* Model monitoring (drift detection)
* A/B testing model deployment

---

# 10. Design Principles

* Single Responsibility per module
* Model-agnostic inference layer
* Reproducible experiments
* Separation between research and production code
* Decision-first (bukan model-first)

---

# 11. Summary

Sistem ini dirancang sebagai:

> Industrial decision support system berbasis telemetry data dan machine learning

Dengan fokus utama:

* Prediksi operasional
* Interpretasi efisiensi
* Rekomendasi tindakan
* Skalabilitas ke sistem produksi
