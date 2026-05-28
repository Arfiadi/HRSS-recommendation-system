"""
Model Evaluator — Mengevaluasi performa model ML secara komprehensif.

File ini akan berisi:
- Menghitung metrik utama: F1-score (macro), ROC-AUC
- Menghitung metrik risiko: False Negative Rate (FNR), False Positive Rate (FPR)
- Menghitung metrik sekunder: Precision & Recall untuk class 1 (optimized)
- Menghasilkan classification report lengkap
- Membuat confusion matrix dan visualisasi evaluasi

Contoh fungsi:
    def evaluate_model(y_true, y_pred, y_proba) -> dict:
        \'\'\'
        Menghitung semua metrik evaluasi dan mengembalikan dictionary:
        {"f1_macro": ..., "roc_auc": ..., "fnr": ..., "fpr": ..., ...}
        \'\'\'
        pass

    def generate_evaluation_report(metrics: dict, output_path: str):
        \'\'\'Membuat laporan evaluasi dalam format markdown.\'\'\'
        pass

TODO: Implement model evaluation functions.
"""
