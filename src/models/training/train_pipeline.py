"""
Train Pipeline (Model Layer) — Proses pelatihan model Random Forest.

Berdasarkan keputusan pada fase eksperimen (Notebook 03 & 04),
Random Forest dipilih sebagai model final karena keandalan
dan kemudahan interpretasinya.
"""
import logging
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)


def train_random_forest(
    X_train,
    y_train,
    n_estimators: int = 100,
    random_state: int = 42,
):
    """
    Melatih RandomForestClassifier sesuai konfigurasi.

    Args:
        X_train: DataFrame fitur training.
        y_train: Array target training.
        n_estimators: Jumlah pohon keputusan.
        random_state: Seed reprodusibilitas.

    Returns:
        Model RandomForestClassifier yang sudah dilatih.
    """
    logger.info(
        "Training RandomForest — n_estimators=%d, seed=%d, features=%d",
        n_estimators, random_state, X_train.shape[1],
    )

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    logger.info("Training complete.")
    return model
