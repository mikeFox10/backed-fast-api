from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioWithRelations
)
from app.services.usuario_service import UsuarioService
from app.models.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=List[UsuarioResponse])
async def get_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener lista de usuarios"""
    usuarios = UsuarioService.get_usuarios(db, skip=skip, limit=limit, search=search)
    return [UsuarioResponse.model_validate(u) for u in usuarios]


@router.get("/{usuario_id}", response_model=UsuarioWithRelations)
async def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener usuario por ID"""
    usuario = UsuarioService.get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Cargar relaciones
    from app.schemas.rol import RolSimple
    from app.schemas.modulo import ModuloSimple
    from app.schemas.persona import PersonaResponse
    
    response = UsuarioWithRelations.model_validate(usuario)
    
    # Obtener roles del usuario
    response.roles = [
        RolSimple.model_validate(ur.rol) 
        for ur in usuario.roles 
        if ur.is_active and ur.rol.is_active
    ]
    
    # Obtener módulos calculados desde roles
    modulos = UsuarioService.get_modulos_from_roles(db, usuario_id)
    response.modulos = [ModuloSimple.model_validate(m) for m in modulos]
    
    if usuario.persona:
        response.persona = PersonaResponse.model_validate(usuario.persona)
    
    return response


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Crear nuevo usuario"""
    nuevo_usuario = UsuarioService.create_usuario(db, usuario)
    # Asignar roles si se proporcionaron
    if usuario.rol_ids:
        UsuarioService.asignar_roles(db, nuevo_usuario.id, usuario.rol_ids)
        db.refresh(nuevo_usuario)
    return UsuarioResponse.model_validate(nuevo_usuario)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar usuario"""
    # Solo superusuarios o el mismo usuario pueden actualizar
    if not current_user.is_superuser and current_user.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este usuario"
        )
    
    usuario = UsuarioService.update_usuario(db, usuario_id, usuario_update)
    return UsuarioResponse.model_validate(usuario)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Eliminar usuario"""
    UsuarioService.delete_usuario(db, usuario_id)
    return None


@router.post("/{usuario_id}/roles", response_model=UsuarioWithRelations)
async def asignar_roles_usuario(
    usuario_id: int,
    rol_ids: List[int],
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Asignar roles a usuario (los módulos se calculan automáticamente desde los roles)"""
    usuario = UsuarioService.asignar_roles(db, usuario_id, rol_ids)
    
    from app.schemas.rol import RolSimple
    from app.schemas.modulo import ModuloSimple
    from app.schemas.persona import PersonaResponse
    
    response = UsuarioWithRelations.model_validate(usuario)
    
    # Obtener roles del usuario
    response.roles = [
        RolSimple.model_validate(ur.rol) 
        for ur in usuario.roles 
        if ur.is_active and ur.rol.is_active
    ]
    
    # Obtener módulos calculados desde roles
    modulos = UsuarioService.get_modulos_from_roles(db, usuario_id)
    response.modulos = [ModuloSimple.model_validate(m) for m in modulos]
    
    if usuario.persona:
        response.persona = PersonaResponse.model_validate(usuario.persona)
    
    return response
