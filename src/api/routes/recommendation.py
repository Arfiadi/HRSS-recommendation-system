"""
Recommendation Endpoint — Endpoint untuk rekomendasi operasional.
"""
from fastapi import APIRouter, Request, HTTPException
from src.api.schemas.request import RecommendationRequest
from src.api.schemas.response import RecommendationResponse

router = APIRouter()


@router.post("/recommend", response_model=RecommendationResponse, tags=["Recommendation"])
def recommend(request: Request, payload: RecommendationRequest):
    service = getattr(request.app.state, "inference_service", None)
    if not service:
        raise HTTPException(
            status_code=503,
            detail="Model service not available. Model loading might have failed.",
        )

    try:
        telemetry_dict = payload.telemetry.model_dump()
        current_mode = payload.current_mode
        result = service.run_inference(telemetry_dict, current_mode=current_mode)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
