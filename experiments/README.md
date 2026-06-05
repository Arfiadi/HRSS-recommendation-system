# Data Science Experiments & MLflow Runs

Folder `experiments/` ini difungsikan khusus sebagai "laboratorium" untuk para *Data Scientist* dan ML Engineers pada tahap *prototyping* dan eksplorasi, sebelum suatu logika diubah menjadi kode Python operasional (production code) di folder `src/`.

## 📒 Alur Jupyter Notebooks (`notebooks/`)

Harap menjalankan dan menelusuri isi notebook secara berurutan untuk memahami *thought process* riset dari proyek HRSS Recommendation System:

1. **`01_data_understanding.ipynb`**: Eksplorasi Data Analisis (EDA), mengecek korelasi statistik antara pola pergerakan, dan memahami bagaimana distribusi *voltage* serta daya listrik yang digunakan alat pada mode *standard* vs *optimized*.
2. **`02_feature_engineering.ipynb`**: Memformulasikan pembuatan metrik turunan yang bernilai secara operasional seperti *Total Power*, *Power Efficiency Ratio*, atau *Movement Variance*. Logika yang stabil di notebook ini di-*porting* (dipindahkan) ke `src/data/feature_engineering.py`.
3. **`03_model_experiments.ipynb`**: Eksperimen melatih banyak tipe algoritma menggunakan **PyCaret**. Mencari model mana (Logistic Regression, RandomForest, dll.) yang memberikan ROC-AUC paling bagus.
4. **`04_model_evaluation_comparison.ipynb`**: Penggalian analitik mendalam pada klasifikasi yang salah (False Positives dan False Negatives) menggunakan MLflow, Learning Curves, dan matriks kebingungan.
5. **`05_recommendation_engine.ipynb`**: Menyimulasikan performa algoritma berbasis aturan bisnis (Rule Engine) ketika diintegrasikan dengan skor dari Machine Learning sebelum digabung menjadi sistem final.

## 📈 MLruns (`mlruns/` & `mlflow.db`)

Semua eksekusi dari notebook 03 & 04 (maupun dari pipeline produksi `train_pipeline.py`) akan mencatatkan log parameternya, metrik performa, dan visualisasinya di dalam database MLflow di root directory dan artifact-nya disimpan di folder `mlruns/`.

**Cara melihat hasilnya:**
Jalankan command ini di root terminal Anda:
```bash
mlflow ui
```
Buka browser pada alamat `http://localhost:5000` untuk membandingkan model Anda secara interaktif.
