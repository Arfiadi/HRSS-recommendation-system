"""
Rule Engine — Logika rekomendasi berbasis aturan domain industri.

File ini berisi evaluasi aturan berbasis domain knowledge untuk HRSS
seperti extreme power load, voltage sag under load, dan smart routing opportunity.

Threshold ditentukan berdasarkan analisis empiris distribusi data:
- total_power: mean ~46000W, P95 ~70000W, P99 ~78000W, max ~112000W
- Voltage per-axis (saat aktif): mean ~50V, P5 ~23V, min 0V
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class HRSSRuleEngine:
    def __init__(self):
        # Thresholds berdasarkan analisis empiris distribusi data HRSS
        self.rules_config = {
            # Rule 1: Extreme Power Load — di atas P97 distribusi total_power
            "total_power_extreme": 75000,
            # Rule 2: Voltage Sag — tegangan motor rel turun saat menarik daya besar
            "rail_motor_power_active": 5000,    # Watt — motor rel dianggap aktif
            "rail_voltage_sag_threshold": 20.0,  # Volt — batas drop tegangan kritis
        }

    def evaluate_rules(self, df: pd.DataFrame) -> list:
        """
        Domain Knowledge Engine: Evaluasi anomali kelistrikan spesifik HRSS.

        Args:
            df: DataFrame satu baris yang berisi metrik engineered & raw.

        Returns:
            Daftar string berisi alert/peringatan teknis yang terpicu.
        """
        alerts = []

        # Rule 1: Extreme Power Load
        # Terpicu jika total konsumsi daya seluruh motor melampaui batas P97.
        if "total_power" in df.columns:
            tot_pwr = df["total_power"].values[0]
            if tot_pwr > self.rules_config["total_power_extreme"]:
                alerts.append(
                    "Extreme Power Load: Total power consumption across all axes "
                    f"is exceptionally high ({tot_pwr:.0f}W). This may indicate "
                    "simultaneous heavy-load movements. Consider staggering "
                    "operations to reduce peak power demand."
                )

        # Rule 2: Voltage Sag Under Load (Rail Motors HL & HR)
        # Terpicu jika motor rel utama menarik daya besar NAMUN tegangannya
        # turun di bawah batas kritis — indikasi ketidakstabilan kelistrikan.
        hl_pwr_col = "O_w_HL_power"
        hl_vlt_col = "O_w_HL_voltage"
        hr_pwr_col = "O_w_HR_power"
        hr_vlt_col = "O_w_HR_voltage"

        required_cols = {hl_pwr_col, hl_vlt_col, hr_pwr_col, hr_vlt_col}
        if required_cols.issubset(df.columns):
            for axis, pcol, vcol in [("HL", hl_pwr_col, hl_vlt_col),
                                      ("HR", hr_pwr_col, hr_vlt_col)]:
                pwr = df[pcol].values[0]
                vlt = df[vcol].values[0]
                if (pwr > self.rules_config["rail_motor_power_active"]
                        and vlt < self.rules_config["rail_voltage_sag_threshold"]):
                    alerts.append(
                        f"Voltage Sag ({axis}): Rail motor {axis} is drawing "
                        f"{pwr:.0f}W but voltage has dropped to {vlt:.1f}V. "
                        "This indicates electrical instability under heavy load. "
                        "Consider switching to Standard routing to stabilize power delivery."
                    )

        logger.info("Rule evaluation complete. Alerts triggered: %d", len(alerts))
        return alerts

