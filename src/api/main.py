"""FastAPI main application for AI Voice Detection API."""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.api.routes import router
from src.api.models import ErrorResponse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Voice Detection API",
    description="Detect whether voice samples are AI-generated or human-spoken",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for public access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for hackathon/public deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "AI Voice Detection API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "voice_detection": "/api/voice-detection",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring."""
    return {
        "status": "healthy",
        "service": "ai-voice-detection-api"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: FastAPI request
        exc: Exception that was raised
        
    Returns:
        JSON error response
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "Internal server error occurred"
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup message."""
    logger.info("=" * 50)
    logger.info("AI Voice Detection API Starting...")
    logger.info("=" * 50)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown message."""
    logger.info("AI Voice Detection API Shutting Down...")


if __name__ == "__main__":
    import uvicorn
    from src.config import HOST, PORT
    
    uvicorn.run(
        "src.api.main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
