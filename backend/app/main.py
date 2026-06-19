from app.api.routes.fir import router as fir_router
from app.api.routes.investigation import router as investigation_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.forthright import router as forthright_router
from app.api.routes.evidence_routes import router as evidence_router

from app.models.qwen_loader import warm_qwen_model, get_model_status
from app.rag.embedder import warm_embedding_model
from app.db.database import engine, Base
import app.db.models as db_models

from backend.app.api.routes.fir import router as fir_router
from backend.app.api.routes.investigation import (
    router as investigation_router
)
from backend.app.api.routes.dashboard import (
    router as dashboard_router
)
from backend.app.api.routes.forthright import (
    router as forthright_router
)
from backend.app.api.routes.evidence_routes import (
    router as evidence_router
)
from backend.app.models.qwen_loader import (
    warm_qwen_model,
    get_model_status
)
from backend.app.rag.embedder import (
    warm_embedding_model
)
from backend.app.db.database import engine, Base
import backend.app.db.models as db_models

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger("fir_copilot.main")

app = FastAPI(
    title="FIR Copilot API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fir_router,
    prefix="/api"
)

app.include_router(
    investigation_router,
    prefix="/api/investigation",
    tags=["Investigation"]
)

app.include_router(
    dashboard_router,
    prefix="/api"
)

app.include_router(
    forthright_router,
    prefix="/api"
)

app.include_router(
    evidence_router,
    prefix="/api",
    tags=["Evidence"]
)


@app.on_event("startup")
def warm_models():
    # 1. Initialize PostgreSQL tables
    try:
        logger.info("Initializing PostgreSQL database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except Exception as error:
        logger.error("Database initialization failed: %s", error)

    # 2. Warm up Qwen model
    try:
        warm_qwen_model()
        logger.info("Qwen model warmed and kept alive")
    except Exception as error:
        logger.warning(
            "Qwen warmup failed: %s",
            error
        )

    # 3. Warm up Embedding model
    try:
        warm_embedding_model()
        logger.info("Embedding model warmed")
    except Exception as error:
        logger.warning(
            "Embedding warmup failed: %s",
            error
        )


@app.get("/")
def home():
    return {
        "message": "FIR Copilot Running"
    }


@app.get("/api/health")
def health_check():
    qwen_status = get_model_status()
    import torch
    cuda_status = torch.cuda.is_available()
    return {
        "status": "healthy" if qwen_status.get("status") == "healthy" else "degraded",
        "qwen": qwen_status,
        "cuda_available": cuda_status,
        "database": "connected"
    }
