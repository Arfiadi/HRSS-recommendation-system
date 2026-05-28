"""
Prediction Service — Reusable logic untuk prediksi ML.

File ini membungkus logika prediksi yang bisa dipanggil dari mana saja
(API, Streamlit, pipeline, notebook) tanpa duplikasi kode.

Tanggung jawab:
- Memuat model yang sudah terlatih
- Menjalankan prediksi pada data input
- Mengembalikan hasil prediksi + probabilitas

Contoh fungsi:
    class PredictionService:
        def __init__(self):
            self.model = load_model()

        def predict(self, features: pd.DataFrame) -> dict:
            \'\'\'
            Mengembalikan:
            {"prediction": int, "probability": float}
            \'\'\'
            pass

        def preprocess(self, raw_input: dict) -> pd.DataFrame:
            \'\'\'Preprocess raw input menjadi feature DataFrame.\'\'\'
            pass

TODO: Implement prediction service.
"""
