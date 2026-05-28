"""
Problem Definition — Definisi formal masalah ML pada proyek HRSS.

File ini akan berisi:
- Definisi target variable (operation_type: 0=standard, 1=optimized)
- Daftar input features (movement, power, voltage columns)
- Daftar engineered features (total_power, rail_activity, dll)
- Definisi evaluation metrics dan threshold keberhasilan
- Mapping label kelas ke deskripsi bisnis

Contoh struktur:
    TARGET_COLUMN = "operation_type"
    CLASS_LABELS = {0: "standard_operation", 1: "optimized_operation"}

    MOVEMENT_COLUMNS = ["I_w_BLO_Weg", "I_w_BHL_Weg", "I_w_BHR_Weg", ...]
    POWER_COLUMNS = ["O_w_BLO_power", "O_w_BHR_power", "O_w_HR_power", ...]
    VOLTAGE_COLUMNS = ["O_w_BLO_voltage", "O_w_HR_voltage", ...]

    SUCCESS_CRITERIA = {
        "f1_macro_min": 0.85,
        "roc_auc_min": 0.90,
    }

TODO: Implement problem definition constants and mappings.
"""
