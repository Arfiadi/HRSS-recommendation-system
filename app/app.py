"""
Streamlit App — Entry point utama dashboard HRSS.

File ini akan berisi:
- Konfigurasi halaman Streamlit (page title, layout, icon)
- Sidebar navigation untuk berpindah antar halaman
- Import dan routing ke halaman: overview, prediction, recommendation,
  model_comparison, explainability

Contoh struktur:
    import streamlit as st

    st.set_page_config(
        page_title="HRSS Recommendation System",
        page_icon="⚙️",
        layout="wide"
    )

    page = st.sidebar.selectbox("Navigation", [
        "Overview", "Prediction", "Recommendation",
        "Model Comparison", "Explainability"
    ])

TODO: Implement Streamlit main app with navigation.
"""
