"""
Training Pipeline — Orchestration alur training end-to-end.

File ini adalah ORKESTRATOR yang mengatur urutan pemanggilan
modul-modul lain untuk proses training.

Alur:
    1. Load raw data          (src/data/ingestion)
    2. Preprocess & clean     (src/data/preprocessing)
    3. Feature engineering     (src/data/feature_engineering)
    4. Train-test split       (src/data/split)
    5. Model training         (src/models/training)
    6. Evaluation             (src/evaluation/evaluator)
    7. MLflow logging         (src/tracking/mlflow_config)
    8. Model registry         (src/models/registry)

Contoh fungsi:
    def run_training_pipeline(config: dict):
        \'\'\'
        Menjalankan seluruh alur training dari data mentah
        hingga model terdaftar di registry.
        \'\'\'
        raw_data = load_raw_datasets(config["raw_dir"])
        clean_data = preprocess(raw_data)
        featured_data = build_features(clean_data)
        X_train, X_test, y_train, y_test = split(featured_data)
        model = train_model(X_train, y_train)
        metrics = evaluate(model, X_test, y_test)
        log_to_mlflow(model, metrics)
        register_model(model, metrics)

TODO: Implement training pipeline orchestration.
"""
