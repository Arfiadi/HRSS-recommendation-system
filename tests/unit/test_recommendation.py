"""
Unit Test — Recommendation Module.
"""
import pandas as pd
from src.recommendation.rule_engine import HRSSRuleEngine
from src.recommendation.decision_policy import generate_decision
from src.recommendation.scoring import calculate_efficiency_score


def test_rule_engine_normal():
    engine = HRSSRuleEngine()
    # Data normal: daya wajar, tegangan stabil
    df = pd.DataFrame(
        [
            {
                "total_power": 45000.0,
                "avg_voltage": 28.0,
                "O_w_HL_power": 12000.0,
                "O_w_HL_voltage": 26.0,
                "O_w_HR_power": 10000.0,
                "O_w_HR_voltage": 26.0,
            }
        ]
    )
    alerts = engine.evaluate_rules(df)
    assert len(alerts) == 0


def test_rule_engine_anomalies():
    engine = HRSSRuleEngine()

    # Test Rule 1: Extreme Power Load (total_power > 75000)
    df_power = pd.DataFrame(
        [
            {
                "total_power": 80000.0,
            }
        ]
    )
    alerts_power = engine.evaluate_rules(df_power)
    assert any("Extreme Power Load" in alert for alert in alerts_power)

    # Test Rule 2: Voltage Sag Under Load (HL motor active but voltage dropped)
    df_voltage = pd.DataFrame(
        [
            {
                "O_w_HL_power": 8000.0,   # > 5000 (active)
                "O_w_HL_voltage": 15.0,    # < 20 (sag!)
                "O_w_HR_power": 200.0,     # inactive
                "O_w_HR_voltage": 0.0,
            }
        ]
    )
    alerts_voltage = engine.evaluate_rules(df_voltage)
    assert any("Voltage Sag (HL)" in alert for alert in alerts_voltage)
    # HR should NOT trigger because power is below active threshold
    assert not any("Voltage Sag (HR)" in alert for alert in alerts_voltage)


def test_decision_policy():
    # Skenario 1: Normal
    risk, action = generate_decision("Standard", "Standard", 0.1, [])
    assert risk == "Optimal Efficiency"

    # Skenario 2: Medium Inefficiency (ML beda, no alerts)
    risk, action = generate_decision("Standard", "Optimized", 0.9, [])
    assert risk == "Sub-optimal Movement"

    # Skenario 3: High Inefficiency (Alerts terpicu)
    risk, action = generate_decision(
        "Optimized", "Standard", 0.1, ["Extreme Power Load alert"]
    )
    assert risk == "Critical Inefficiency"


def test_scoring():
    df = pd.DataFrame([{}])
    # Case 1: Optimized prob 80%, no alerts
    score = calculate_efficiency_score(df, 0.8, [])
    assert score == 80.0

    # Case 2: Penalti dari Extreme Power Load (80% - 25% = 55%)
    score = calculate_efficiency_score(df, 0.8, ["Extreme Power Load alert"])
    assert score == 55.0

    # Case 3: Penalti dari Voltage Sag (80% - 30% = 50%)
    score = calculate_efficiency_score(df, 0.8, ["Voltage Sag (HL): alert"])
    assert score == 50.0

    # Case 4: Batas bawah 0%
    score = calculate_efficiency_score(
        df, 0.2, ["Extreme Power Load alert", "Voltage Sag (HL): alert"]
    )
    assert score == 0.0

