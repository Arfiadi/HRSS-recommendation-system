"""
UI Helpers — Komponen visual reusable untuk Streamlit dashboard.

File ini akan berisi:
- Fungsi untuk menampilkan metric cards
- Fungsi untuk menampilkan recommendation cards dengan warna risiko
- Fungsi untuk menampilkan comparison tables (raw vs engineered)
- Loading spinners dan progress indicators

Contoh fungsi:
    def show_metric_card(title: str, value: str, delta: str = None):
        \'\'\'Menampilkan metric card dengan styling custom.\'\'\'
        st.metric(label=title, value=value, delta=delta)

    def show_recommendation_card(risk_level: str, recommendations: list):
        \'\'\'Menampilkan card rekomendasi dengan warna sesuai risk level.\'\'\'
        pass

TODO: Implement UI helper components.
"""
