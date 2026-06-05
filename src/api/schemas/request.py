"""
Request Schemas — Pydantic model untuk validasi input API.
"""
from pydantic import BaseModel, Field
from typing import Optional


class TelemetryInput(BaseModel):
    Timestamp: float = Field(..., description="Timestamp pencatatan data telemetry")

    # Movement Columns (Weg / displacement)
    I_w_BLO_Weg: float = Field(..., description="Sumbu conveyor Weg")
    I_w_BHL_Weg: float = Field(..., description="Sumbu lift kiri Weg")
    I_w_BHR_Weg: float = Field(..., description="Sumbu lift kanan Weg")
    I_w_BRU_Weg: float = Field(..., description="Sumbu rotary Weg")
    I_w_HR_Weg: float = Field(..., description="Sumbu rel kanan Weg")
    I_w_HL_Weg: float = Field(..., description="Sumbu rel kiri Weg")

    # Power Columns
    O_w_BLO_power: float = Field(..., description="Sumbu conveyor power")
    O_w_BHL_power: float = Field(..., description="Sumbu lift kiri power")
    O_w_BHR_power: float = Field(..., description="Sumbu lift kanan power")
    O_w_BRU_power: float = Field(..., description="Sumbu rotary power")
    O_w_HR_power: float = Field(..., description="Sumbu rel kanan power")
    O_w_HL_power: float = Field(..., description="Sumbu rel kiri power")

    # Voltage Columns
    O_w_BLO_voltage: float = Field(..., description="Sumbu conveyor voltage")
    O_w_BHL_voltage: float = Field(..., description="Sumbu lift kiri voltage")
    O_w_BHR_voltage: float = Field(..., description="Sumbu lift kanan voltage")
    O_w_BRU_voltage: float = Field(..., description="Sumbu rotary voltage")
    O_w_HR_voltage: float = Field(..., description="Sumbu rel kanan voltage")
    O_w_HL_voltage: float = Field(..., description="Sumbu rel kiri voltage")

    # Optional pre-computed engineered features
    total_power: Optional[float] = Field(None, description="Pre-calculated total power")
    avg_voltage: Optional[float] = Field(None, description="Pre-calculated average voltage")
    total_movement: Optional[float] = Field(None, description="Pre-calculated total movement")
    power_efficiency_ratio: Optional[float] = Field(None, description="Pre-calculated power efficiency ratio")
    rail_activity: Optional[float] = Field(None, description="Pre-calculated rail activity")
    conveyor_activity: Optional[float] = Field(None, description="Pre-calculated conveyor activity")


class RecommendationRequest(BaseModel):
    telemetry: TelemetryInput = Field(..., description="Data telemetry aktual sensor IoT")
    current_mode: str = Field("Standard", description="Mode operasional mesin saat ini (Standard / Optimized)")
