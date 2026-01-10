import logging
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.core.middleware import (
    LoggingMiddleware,
    ErrorHandlingMiddleware,
    setup_cors
)
from app.api.v1 import api_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Usuarios y Permisos",
    description="API REST profesional con FastAPI para gestión de usuarios, roles, módulos y permisos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json"
)

# Configurar middlewares
setup_cors(app)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# Incluir routers
app.include_router(api_router)


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Sistema de Gestión de Usuarios y Permisos API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
