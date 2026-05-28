"""
Response Schemas — Pydantic model untuk format output API.

Contoh:
    class PredictionResponse(BaseModel):
        prediction: int           # 0 or 1
        probability: float        # 0.0 - 1.0
        risk_level: str           # low / medium / high
        recommendation: str       # actionable suggestion

TODO: Implement response schemas.
"""
