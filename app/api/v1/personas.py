from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser
from app.schemas.persona import (
    PersonaCreate,
    PersonaUpdate,
    PersonaResponse
)
from app.services.persona_service import PersonaService
from app.models.usuario import Usuario

router = APIRouter(prefix="/personas", tags=["Personas"])


@router.get("/usuario/{usuario_id}", response_model=PersonaResponse)
async def get_persona_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener persona de un usuario"""
    # Solo superusuarios o el mismo usuario pueden ver los datos
    if not current_user.is_superuser and current_user.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver estos datos"
        )
    
    persona = PersonaService.get_persona(db, usuario_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )
    
    return PersonaResponse.model_validate(persona)


@router.get("/me", response_model=PersonaResponse)
async def get_mi_persona(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener mi propia persona"""
    persona = PersonaService.get_persona(db, current_user.id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes datos personales registrados"
        )
    
    return PersonaResponse.model_validate(persona)


@router.post("/usuario/{usuario_id}", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
async def create_persona(
    usuario_id: int,
    datos: PersonaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear persona para un usuario"""
    # Solo superusuarios o el mismo usuario pueden crear persona
    if not current_user.is_superuser and current_user.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear estos datos"
        )
    
    persona = PersonaService.create_persona(db, usuario_id, datos)
    return PersonaResponse.model_validate(persona)


@router.post("/me", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
async def create_mi_persona(
    datos: PersonaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear mi propia persona"""
    persona = PersonaService.create_persona(db, current_user.id, datos)
    return PersonaResponse.model_validate(persona)


@router.put("/usuario/{usuario_id}", response_model=PersonaResponse)
async def update_persona(
    usuario_id: int,
    datos_update: PersonaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar persona de un usuario"""
    # Solo superusuarios o el mismo usuario pueden actualizar
    if not current_user.is_superuser and current_user.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar estos datos"
        )
    
    persona = PersonaService.update_persona(db, usuario_id, datos_update)
    return PersonaResponse.model_validate(persona)


@router.put("/me", response_model=PersonaResponse)
async def update_mi_persona(
    datos_update: PersonaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar mi propia persona"""
    persona = PersonaService.update_persona(db, current_user.id, datos_update)
    return PersonaResponse.model_validate(persona)


@router.delete("/usuario/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_persona(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Eliminar persona de un usuario (solo superusuarios)"""
    PersonaService.delete_persona(db, usuario_id)
    return None
