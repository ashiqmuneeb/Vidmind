from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging, logger
from backend.app.core.exceptions import VidMindException
from backend.app.db.database import init_db

# Import routers
from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.videos import router as videos_router
from backend.app.api.routes.processing import router as processing_router
from backend.app.api.routes.transcripts import router as transcripts_router
from backend.app.api.routes.notes import router as notes_router
from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.search import router as search_router
from backend.app.api.routes.exports import router as exports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode...")
    await init_db()
    # Ensure data directory structure exists
    settings.data_path
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    description="VidMind — AI Long-Video Transcription, Understanding, Notes & Q&A Platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Exception Handler
@app.exception_handler(VidMindException)
async def vidmind_exception_handler(request: Request, exc: VidMindException):
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": exc.message, "details": exc.details},
    )

# Include API Routers under /api
app.include_router(health_router, prefix="/api")
app.include_router(videos_router, prefix="/api")
app.include_router(processing_router, prefix="/api")
app.include_router(transcripts_router, prefix="/api")
app.include_router(notes_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(exports_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
    }
