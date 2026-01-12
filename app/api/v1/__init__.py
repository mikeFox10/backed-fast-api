from fastapi import APIRouter
from app.api.v1 import auth, usuarios, roles, modulos, permisos, personas

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/api/v1")
api_router.include_router(usuarios.router, prefix="/api/v1")
api_router.include_router(roles.router, prefix="/api/v1")
api_router.include_router(modulos.router, prefix="/api/v1")
api_router.include_router(permisos.router, prefix="/api/v1")
api_router.include_router(personas.router, prefix="/api/v1")