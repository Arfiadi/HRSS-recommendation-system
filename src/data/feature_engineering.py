"""
Feature Engineering — Membuat fitur turunan dari data telemetry HRSS.

File ini akan berisi:
- Perhitungan total_power (agregasi kolom power)
- Perhitungan avg_voltage (rata-rata kolom voltage)
- Perhitungan total_movement (agregasi kolom movement/Weg)
- Perhitungan rail_activity dan conveyor_activity
- Perhitungan energy_efficiency_ratio
- Fungsi utama build_features() yang menjalankan semua di atas

Contoh fungsi:
    def build_features(df: pd.DataFrame) -> pd.DataFrame:
        \'\'\'
        Membuat fitur-fitur turunan:
        - total_power, avg_voltage
        - total_movement, rail_activity, conveyor_activity
        - energy_efficiency_ratio
        \'\'\'
        df["total_power"] = df[POWER_COLUMNS].sum(axis=1)
        df["rail_activity"] = df[["I_w_HR_Weg", "I_w_HL_Weg"]].sum(axis=1)
        ...
        return df

TODO: Implement feature engineering functions.
"""
