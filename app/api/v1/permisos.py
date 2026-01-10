from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser
from app.schemas.permiso import PermisoCreate, PermisoUpdate, PermisoResponse, PermisoWithRelations
from app.services.permiso_service import PermisoService
from app.models.usuario import Usuario

router = APIRouter(prefix="/permisos", tags=["Permisos"])


@router.get("", response_model=List[PermisoResponse])
async def get_permisos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener lista de permisos"""
    permisos = PermisoService.get_permisos(db, skip=skip, limit=limit, is_active=is_active)
    return [PermisoResponse.model_validate(p) for p in permisos]


@router.get("/{permiso_id}", response_model=PermisoWithRelations)
async def get_permiso(
    permiso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener permiso por ID"""
    permiso = PermisoService.get_permiso(db, permiso_id)
    if not permiso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permiso no encontrado"
        )
    
    response = PermisoWithRelations.model_validate(permiso)
    response.roles_count = len([rp for rp in permiso.roles if rp.is_active])
    response.modulos_count = len([mp for mp in permiso.modulos if mp.is_active])
    
    return response


@router.post("", response_model=PermisoResponse, status_code=status.HTTP_201_CREATED)
async def create_permiso(
    permiso: PermisoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Crear nuevo permiso"""
    nuevo_permiso = PermisoService.create_permiso(db, permiso)
    return PermisoResponse.model_validate(nuevo_permiso)


@router.put("/{permiso_id}", response_model=PermisoResponse)
async def update_permiso(
    permiso_id: int,
    permiso_update: PermisoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Actualizar permiso"""
    permiso = PermisoService.update_permiso(db, permiso_id, permiso_update)
    return PermisoResponse.model_validate(permiso)


@router.delete("/{permiso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permiso(
    permiso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Eliminar permiso"""
    PermisoService.delete_permiso(db, permiso_id)
    return None
