"""
Prediction Endpoint — Endpoint untuk menerima data dan mengembalikan prediksi.
"""
from fastapi import APIRouter, Request, HTTPException
from src.api.schemas.request import TelemetryInput
from src.api.schemas.response import PredictionResponse

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(request: Request, payload: TelemetryInput):
    service = getattr(request.app.state, "inference_service", None)
    if not service:
        raise HTTPException(
            status_code=503,
            detail="Model service not available. Model loading might have failed.",
        )

    try:
        telemetry_dict = payload.model_dump()
        result = service.prediction_service.predict(telemetry_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
