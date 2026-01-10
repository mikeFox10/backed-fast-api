from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser
from app.schemas.rol import RolCreate, RolUpdate, RolResponse, RolWithRelations
from app.services.rol_service import RolService
from app.models.usuario import Usuario

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=List[RolResponse])
async def get_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener lista de roles"""
    roles = RolService.get_roles(db, skip=skip, limit=limit, is_active=is_active)
    return [RolResponse.model_validate(r) for r in roles]


@router.get("/{rol_id}", response_model=RolWithRelations)
async def get_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener rol por ID"""
    rol = RolService.get_rol(db, rol_id)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    from app.schemas.permiso import PermisoSimple
    
    response = RolWithRelations.model_validate(rol)
    response.permisos = [PermisoSimple.model_validate(rp.permiso) for rp in rol.permisos if rp.is_active]
    response.usuarios_count = len(rol.usuarios)
    
    return response


@router.post("", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
async def create_rol(
    rol: RolCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Crear nuevo rol"""
    nuevo_rol = RolService.create_rol(db, rol)
    return RolResponse.model_validate(nuevo_rol)


@router.put("/{rol_id}", response_model=RolResponse)
async def update_rol(
    rol_id: int,
    rol_update: RolUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Actualizar rol"""
    rol = RolService.update_rol(db, rol_id, rol_update)
    return RolResponse.model_validate(rol)


@router.delete("/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Eliminar rol"""
    RolService.delete_rol(db, rol_id)
    return None


@router.post("/{rol_id}/permisos", response_model=RolWithRelations)
async def asignar_permisos_rol(
    rol_id: int,
    permiso_ids: List[int],
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Asignar permisos a rol"""
    rol = RolService.asignar_permisos(db, rol_id, permiso_ids)
    
    from app.schemas.permiso import PermisoSimple
    
    response = RolWithRelations.model_validate(rol)
    response.permisos = [PermisoSimple.model_validate(rp.permiso) for rp in rol.permisos if rp.is_active]
    response.usuarios_count = len(rol.usuarios)
    
    return response
