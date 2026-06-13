"""
Problem Definition — Definisi formal masalah ML pada proyek HRSS.

Modul ini adalah satu-satunya sumber kebenaran (single source of truth) untuk
semua konstanta domain, nama kolom, dan kriteria keberhasilan model.
"""

# =========================================================
# TARGET
# =========================================================
TARGET_COLUMN = "operation_type"
CLASS_LABELS = {0: "standard_operation", 1: "optimized_operation"}

# =========================================================
# RAW SENSOR COLUMNS (from HRSS telemetry CSV)
# =========================================================
MOVEMENT_COLUMNS = [
    "I_w_BLO_Weg", "I_w_BHL_Weg", "I_w_BHR_Weg",
    "I_w_BRU_Weg", "I_w_HR_Weg", "I_w_HL_Weg",
]

POWER_COLUMNS = [
    "O_w_BLO_power", "O_w_BHL_power", "O_w_BHR_power",
    "O_w_BRU_power", "O_w_HR_power", "O_w_HL_power",
]

VOLTAGE_COLUMNS = [
    "O_w_BLO_voltage", "O_w_BHL_voltage", "O_w_BHR_voltage",
    "O_w_BRU_voltage", "O_w_HR_voltage", "O_w_HL_voltage",
]

RAIL_COLUMNS = ["I_w_HL_Weg", "I_w_HR_Weg"]
CONVEYOR_COLUMNS = ["I_w_BLO_Weg", "I_w_BHL_Weg", "I_w_BHR_Weg", "I_w_BRU_Weg"]

# All raw sensor columns (excluding Timestamp and Labels)
ALL_SENSOR_COLUMNS = MOVEMENT_COLUMNS + POWER_COLUMNS + VOLTAGE_COLUMNS

# =========================================================
# ENGINEERED FEATURE NAMES
# =========================================================
ENGINEERED_FEATURES = [
    "total_power", "avg_voltage", "active_motor_count",
]

# Full feature set used by the model (raw sensors + engineered)
MODEL_FEATURE_COLUMNS = (
    ALL_SENSOR_COLUMNS + ENGINEERED_FEATURES
)

# =========================================================
# RAW DATA FILES
# =========================================================
RAW_FILES = {
    "normal_standard": "HRSS_normal_standard.csv",
    "normal_optimized": "HRSS_normal_optimized.csv",
}

# =========================================================
# SUCCESS CRITERIA (from evaluation_framework.md)
# =========================================================
SUCCESS_CRITERIA = {
    "f1_macro_min": 0.85,
    "roc_auc_min": 0.90,
}
