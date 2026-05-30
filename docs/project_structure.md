# Project Structure — HRSS Recommendation System

## 1. Project Directory Structure

```
HRSS_recommendation_system/
│
├── README.md
├── requirements.txt
├── .gitignore
├── pyproject.toml
│
├── data/
│   ├── raw/
│   │   ├── HRSS_normal_standard.csv
│   │   ├── HRSS_normal_optimized.csv
│   │   ├── HRSS_anomalous_standard.csvV
│   │   ├── HRSS_anomalous_optimized.csv
│   │
│   ├── interim/
│   │   └── (cleaned but not ML-ready data)
│   │
│   ├── processed/
│   │   ├── hrss_clean_integrated_original.csv
│   │   ├── hrss_clean_integrated_engineered.csv
│   │
│   └── splits/                 # SINGLE SOURCE OF TRUTH
│       ├── X_train_raw.csv
│       ├── X_test_raw.csv
│       ├── y_train_raw.csv
│       ├── y_test_raw.csv
│       ├── X_train_eng.csv
│       ├── X_test_eng.csv
│       ├── y_train_eng.csv
│       ├── y_test_eng.csv
│
├── configs/
│   ├── config.yaml
│   ├── model_config.yaml
│   ├── feature_config.yaml
│
├── docs/
│   ├── architecture.md
│   ├── system_design.md
│   ├── evaluation_framework.md
│   ├── business_understanding_and_problem_framing.md
│   ├── model_comparison_report.md
│   ├── recommendation_system_design.md
│   └── archive/
│       └── blueprint.md
│
├── experiments/
│   ├── notebooks/
│   │   ├── 01_data_understanding.ipynb
│   │   ├── 02_feature_engineering.ipynb
│   │   ├── 03_raw_experiment_mlflow.ipynb
│   │   ├── 04_engineered_experiment_mlflow.ipynb
│   │   ├── 05_model_evaluation_comparison.ipynb
│   │   ├── 06_recommendation_engine.ipynb
│   │
│   ├── mlruns/
│
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── prediction.py
│   │   │   ├── recommendation.py
│   │   │   └── health.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── request.py
│   │       └── response.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── domain_schema.py
│   │   ├── problem_definition.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   ├── preprocessing.py
│   │   ├── feature_engineering.py
│   │   ├── split.py
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   ├── evaluator.py
│   │   ├── validation.py
│   │
│   ├── feature_store/
│   │   ├── __init__.py
│   │   ├── store.py
│   │   ├── registry.py
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   ├── feature_builder.py
│   │   ├── feature_validator.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── inference/
│   │   │   ├── __init__.py
│   │   │   ├── model_loader.py
│   │   │   ├── predictor.py
│   │   ├── registry/
│   │   │   ├── __init__.py
│   │   │   ├── model_registry.py
│   │   ├── training/
│   │   │   ├── __init__.py
│   │   │   ├── pycaret_runner.py
│   │   │   ├── train_pipeline.py
│   │
│   ├── recommendation/
│   │   ├── __init__.py
│   │   ├── rule_engine.py
│   │   ├── decision_policy.py
│   │   ├── scoring.py
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── train_pipeline.py
│   │   ├── inference_pipeline.py
│   │   ├── pipeline_utils.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── inference_service.py
│   │   ├── prediction_service.py
│   │   ├── recommendation_service.py
│   │
│   ├── streaming/
│   │   ├── __init__.py
│   │   ├── kafka_consumer.py
│   │   ├── stream_processor.py
│   │
│   ├── tracking/
│   │   ├── __init__.py
│   │   ├── mlflow_config.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   ├── io.py
│   │   ├── logger.py
│
├── tests/
│   ├── conftest.py
│   ├── integration/
│   │   ├── test_pipeline_engineered.py
│   │   ├── test_pipeline_raw.py
│   ├── unit/
│   │   ├── test_feature_engineering.py
│   │   ├── test_inference_service.py
│   │   ├── test_preprocessing.py
│   │   ├── test_recommendation.py
│
├── app/
│   ├── app.py
│   ├── config.py
│   ├── pages/
│   │   ├── overview.py
│   │   ├── prediction.py
│   │   ├── recommendation.py
│   │   ├── model_comparison.py
│   │   ├── explainability.py
│   │
│   ├── components/
│   │   ├── data_loader.py
│   │   ├── model_loader.py
│   │   ├── predictor.py
│   │   ├── recommender.py
│   │   ├── ui_helpers.py
│   │
│   ├── assets/
│       ├── style.css
│
├── outputs/
│   ├── figures/
│   │   ├── confusion_matrix/
│   │   ├── feature_importance/
│   │   ├── shap_values/
│   │
│   ├── models/
│   │   ├── raw/
│   │   ├── engineered/
│   │
│   ├── reports/
│       ├── evaluation_summary.md
│       ├── raw_vs_engineered_comparison.md
│       ├── recommendation_report.md
│       ├── system_design_report.md
│
├── ci_cd/
│   ├── .github/
│   │   └── workflows/
│   │       ├── deploy.yml
│   │       ├── test.yml
│
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── Dockerfile.api
│   ├── docker-compose.yml
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│
└── monitoring/
    ├── alerting.py
    ├── drift_detection.py
    ├── performance_monitoring.py
```

---

## 2. Explanation per Layer

## 2.1 Data Layer

Folder `data/` adalah sumber utama seluruh pipeline ML.

* **raw/** → data asli tanpa perubahan
* **interim/** → data hasil cleaning awal (non-ML ready)
* **processed/** → data siap training (baseline & engineered)
* **splits/** → single source of truth untuk train/test split

👉 Tujuan utama: menjaga reproducibility dan fairness eksperimen raw vs engineered.

---

## 2.2 Config Layer

Folder `configs/` menyimpan semua parameter sistem.

* config.yaml → global settings
* model_config.yaml → hyperparameter & model settings
* feature_config.yaml → feature engineering rules

👉 Menghindari hardcoding dan meningkatkan maintainability.

---

## 2.3 Documentation Layer

Folder `docs/` berisi semua dokumentasi sistem.

* architecture.md → arsitektur sistem
* system_design.md → desain teknis ML system
* evaluation_framework.md → definisi metrik evaluasi
* business_understanding_and_problem_framing.md → konteks bisnis
* model_comparison_report.md → hasil eksperimen
* recommendation_system_design.md → desain logika rekomendasi

👉 Menjadi source of truth non-kode.

---

## 2.4 Experimentation Layer

Folder `experiments/` adalah area eksplorasi.

* notebooks → eksperimen data & model
* mlruns → tracking eksperimen menggunakan MLflow

Urutan eksperimen:

1. data understanding
2. feature engineering
3. raw model experiment
4. engineered model experiment
5. evaluation comparison
6. recommendation prototype

👉 Fokus: eksplorasi, bukan production.

---

## 2.5 Core Source Code (src)

Ini adalah inti sistem produksi. Modul dipisahkan untuk mendukung Separation of Concerns.

### api/
Entry point FastAPI untuk prediction dan recommendation.

### core/
Definisi domain dan problem ML.

### data/
Pipeline data processing end-to-end.

### evaluation/
Sistem evaluasi model: F1, ROC-AUC, Recall dan Precision class 1 FNR, FPR.

### feature_store/
Manajemen fitur terpusat (Future Scale).

### features/
Abstraksi feature engineering.

### models/
* training → PyCaret + training pipeline
* inference → model loading & prediction
* registry → model versioning

### recommendation/
Logika rekomendasi industri:
* rule-based system
* decision policy
* scoring system

### pipeline/
Orchestration layer (alur eksekusi end-to-end):
* train_pipeline → orchestration training flow (data → preprocess → feature → model → evaluate → MLflow)
* inference_pipeline → orchestration inference flow (input → preprocess → predict → recommend)
* pipeline_utils → helper functions untuk pipeline

👉 Pipeline menyusun urutan alur, services menyediakan kemampuan.

### services/
Reusable logic layer:
* inference service → unified entry point
* prediction service → wrapper inference logic (reusable oleh API, Streamlit, pipeline)
* recommendation service → wrapper decision system

### streaming/
Streaming ingestion dan pemrosesan (Future Scale).

### tracking/
MLflow utilities.

### utils/
Utilitas umum (IO, Logging, Configuration).

👉 Ini adalah transisi dari ML project → ML system.

---

## 2.6 Application Layer (app)

UI berbasis Streamlit. UI hanya bertindak sebagai consumer dari service layer.

* overview → sistem overview
* prediction → inference UI
* recommendation → output rekomendasi
* model comparison → hasil eksperimen
* explainability → SHAP / interpretability

---

## 2.7 Outputs Layer

Berisi hasil sistem:

* figures → visualisasi
* models → model artifacts
* reports → laporan evaluasi

👉 Untuk analisis, reporting, dan portfolio.

---

## 2.8 Deployment Layer

Persiapan production system.

* Dockerfile → containerization
* docker-compose → orchestration
* k8s/ → Kubernetes manifests (Future Scale)

---

## 2.9 Monitoring Layer

Untuk industrial-scale ML system.

* drift detection → data shift monitoring
* performance monitoring → model degradation tracking
* alerting.py → Alert system (Future Scale)

---

## 3. Design Principle

Struktur ini mengikuti:

* Separation of Concerns
* Experiment vs Production separation
* Reproducibility (MLflow + splits)
* Service-oriented ML architecture
* Scalability-first design

---

## 4. Summary

Struktur ini mendukung full lifecycle ML system:

Data → Experiment → Model → Service → Application → Deployment → Monitoring

Dan dapat berkembang tanpa refactor besar di masa depan.
