"""FastAPI application factory."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from ..core.config import get_settings
from ..core.logging import setup_logging, get_logger
from .routers import materials, solvents, experiments

setup_logging()
logger = get_logger(__name__)
settings = get_settings()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="CrystalDB API",
        description="Crystallography experiment and data collection system",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.is_development else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(materials.router, prefix="/api/v1/materials", tags=["Materials"])
    app.include_router(solvents.router, prefix="/api/v1/solvents", tags=["Solvents"])
    app.include_router(experiments.router, prefix="/api/v1/experiments", tags=["Experiments"])

    # Mount static files
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    async def root():
        """Serve the web interface."""
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {
            "name": "CrystalDB API",
            "version": "2.0.0",
            "docs": "/docs",
            "web": "/",
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy"}

    logger.info("FastAPI application created successfully")
    return app
