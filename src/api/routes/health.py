"""
Health Check Endpoint — Mengecek status kesehatan sistem.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "HRSS Recommendation System API",
    }
