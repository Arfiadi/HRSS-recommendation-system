"""
Rule Engine — Logika rekomendasi berbasis aturan domain industri.

File ini berisi evaluasi aturan berbasis domain knowledge untuk HRSS
seperti rail inefficiency, mechanical friction/overload, dan DC bus voltage sag.
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class HRSSRuleEngine:
    def __init__(self):
        # Thresholds berdasarkan karakteristik fisik alat HRSS / Stacker Crane
        self.rules_config = {
            "rail_activity_high": 0.05,
            "power_efficiency_low": 0.01,
            "total_power_high": 15.0,
            "total_movement_low": 0.02,
            "avg_voltage_drop": 23.5,  # Batas drop aman DC bus 24V
        }

    def evaluate_rules(self, df: pd.DataFrame) -> list:
        """
        Domain Knowledge Engine: Evaluasi anomali mekanis dan kelistrikan spesifik HRSS.

        Args:
            df: DataFrame satu baris yang berisi metrik engineered & raw.

        Returns:
            Daftar string berisi alert/peringatan teknis yang terpicu.
        """
        alerts = []

        # Rule 1: Rail Inefficiency (Banyak gerak rel horizontal, efisiensi minim)
        if "rail_activity" in df.columns and "power_efficiency_ratio" in df.columns:
            rail_act = df["rail_activity"].values[0]
            pwr_eff = df["power_efficiency_ratio"].values[0]
            if (
                rail_act > self.rules_config["rail_activity_high"]
                and pwr_eff < self.rules_config["power_efficiency_low"]
            ):
                alerts.append(
                    "Rail Inefficiency: Aktivitas sumbu horizontal tinggi namun rasio efisiensi daya sangat rendah. "
                    "Pertimbangkan optimasi algoritma routing (shortest path) pada WMS."
                )

        # Rule 2: Mechanical Friction / Overload (Daya tinggi, pergerakan minim)
        if "total_power" in df.columns and "total_movement" in df.columns:
            tot_pwr = df["total_power"].values[0]
            tot_mvt = df["total_movement"].values[0]
            if (
                tot_pwr > self.rules_config["total_power_high"]
                and tot_mvt < self.rules_config["total_movement_low"]
            ):
                alerts.append(
                    "Overload/Friction Warning: Tarikan total arus/daya tinggi tanpa pergerakan mekanis yang proporsional. "
                    "Lakukan inspeksi keausan guide rail atau cek batas maksimum muatan hoist."
                )

        # Rule 3: Electrical Voltage Drop (DC Bus) (Drop tegangan di bawah batas aman)
        if "avg_voltage" in df.columns:
            avg_volt = df["avg_voltage"].values[0]
            if avg_volt < self.rules_config["avg_voltage_drop"]:
                alerts.append(
                    "Voltage Sag Anomaly: Tegangan rata-rata turun di bawah batas aman. "
                    "Hindari memberikan command akselerasi serentak pada multi-sumbu (X dan Y axis) untuk mencegah trip/reset sistem."
                )

        logger.info("Rule evaluation complete. Alerts triggered: %d", len(alerts))
        return alerts
