from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser
from app.schemas.modulo import ModuloCreate, ModuloUpdate, ModuloResponse, ModuloWithRelations
from app.services.modulo_service import ModuloService
from app.models.usuario import Usuario

router = APIRouter(prefix="/modulos", tags=["Módulos"])


@router.get("", response_model=List[ModuloResponse])
async def get_modulos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener lista de módulos"""
    modulos = ModuloService.get_modulos(
        db, skip=skip, limit=limit, is_active=is_active, parent_id=parent_id
    )
    return [ModuloResponse.model_validate(m) for m in modulos]


@router.get("/{modulo_id}", response_model=ModuloWithRelations)
async def get_modulo(
    modulo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener módulo por ID"""
    modulo = ModuloService.get_modulo(db, modulo_id)
    if not modulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Módulo no encontrado"
        )
    
    from app.schemas.permiso import PermisoSimple
    
    response = ModuloWithRelations.model_validate(modulo)
    response.permisos = [PermisoSimple.model_validate(mp.permiso) for mp in modulo.permisos if mp.is_active]
    response.usuarios_count = len([um for um in modulo.usuarios if um.is_active])
    response.children = [ModuloResponse.model_validate(child) for child in modulo.children]
    
    return response


@router.post("", response_model=ModuloResponse, status_code=status.HTTP_201_CREATED)
async def create_modulo(
    modulo: ModuloCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Crear nuevo módulo"""
    nuevo_modulo = ModuloService.create_modulo(db, modulo)
    return ModuloResponse.model_validate(nuevo_modulo)


@router.put("/{modulo_id}", response_model=ModuloResponse)
async def update_modulo(
    modulo_id: int,
    modulo_update: ModuloUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Actualizar módulo"""
    modulo = ModuloService.update_modulo(db, modulo_id, modulo_update)
    return ModuloResponse.model_validate(modulo)


@router.delete("/{modulo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_modulo(
    modulo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Eliminar módulo"""
    ModuloService.delete_modulo(db, modulo_id)
    return None


@router.post("/{modulo_id}/permisos", response_model=ModuloWithRelations)
async def asignar_permisos_modulo(
    modulo_id: int,
    permiso_ids: List[int],
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superuser)
):
    """Asignar permisos a módulo"""
    modulo = ModuloService.asignar_permisos(db, modulo_id, permiso_ids)
    
    from app.schemas.permiso import PermisoSimple
    
    response = ModuloWithRelations.model_validate(modulo)
    response.permisos = [PermisoSimple.model_validate(mp.permiso) for mp in modulo.permisos if mp.is_active]
    response.usuarios_count = len([um for um in modulo.usuarios if um.is_active])
    
    return response
