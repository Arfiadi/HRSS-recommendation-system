"""
API Main — Entry point FastAPI application.
"""
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Muat environment variables dari .env
load_dotenv()

from src.api.routes.health import router as health_router
from src.api.routes.prediction import router as prediction_router
from src.api.routes.recommendation import router as recommendation_router
from src.services.inference_service import InferenceService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model
    logger.info("FastAPI starting up...")
    try:
        # Mengharuskan pemuatan model lokal (Offline Baking)
        logger.info("Lifespan: Initializing InferenceService with local champion model...")
        app.state.inference_service = InferenceService(
            model_path="models/final_hrss_rf_model.pkl"
        )
        logger.info("Lifespan: InferenceService successfully loaded local model.")
    except Exception as e:
        logger.critical(
            "Lifespan: CRITICAL - Failed to load local champion model! Details: %s. "
            "Offline serving cannot start.",
            str(e)
        )
        app.state.inference_service = None
        raise e

    yield
    # Shutdown logic
    logger.info("FastAPI shutting down...")


app = FastAPI(
    title="HRSS Recommendation System API",
    description="Industrial Operational Recommendation API for HRSS/Stacker Crane Energy Optimization.",
    version="1.0.0",
    lifespan=lifespan,
)

# Konfigurasi CORS agar bisa diakses oleh Frontend (Vite/React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development, izinkan semua port frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrasi routers
app.include_router(health_router)
app.include_router(prediction_router, prefix="/api/v1")
app.include_router(recommendation_router, prefix="/api/v1")
