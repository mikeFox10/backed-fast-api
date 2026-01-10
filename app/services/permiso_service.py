from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.permiso import Permiso
from app.schemas.permiso import PermisoCreate, PermisoUpdate


class PermisoService:
    @staticmethod
    def get_permiso(db: Session, permiso_id: int) -> Optional[Permiso]:
        """Obtener permiso por ID"""
        return db.query(Permiso).filter(Permiso.id == permiso_id).first()

    @staticmethod
    def get_permiso_by_codigo(db: Session, codigo: str) -> Optional[Permiso]:
        """Obtener permiso por código"""
        return db.query(Permiso).filter(Permiso.codigo == codigo).first()

    @staticmethod
    def get_permisos(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[Permiso]:
        """Obtener lista de permisos"""
        query = db.query(Permiso)
        if is_active is not None:
            query = query.filter(Permiso.is_active == is_active)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_permiso(db: Session, permiso: PermisoCreate) -> Permiso:
        """Crear nuevo permiso"""
        if PermisoService.get_permiso_by_codigo(db, permiso.codigo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código del permiso ya existe"
            )
        
        db_permiso = Permiso(
            nombre=permiso.nombre,
            codigo=permiso.codigo,
            descripcion=permiso.descripcion,
            is_active=permiso.is_active
        )
        db.add(db_permiso)
        db.commit()
        db.refresh(db_permiso)
        return db_permiso

    @staticmethod
    def update_permiso(
        db: Session,
        permiso_id: int,
        permiso_update: PermisoUpdate
    ) -> Permiso:
        """Actualizar permiso"""
        db_permiso = PermisoService.get_permiso(db, permiso_id)
        if not db_permiso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permiso no encontrado"
            )
        
        if permiso_update.codigo and permiso_update.codigo != db_permiso.codigo:
            if PermisoService.get_permiso_by_codigo(db, permiso_update.codigo):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El código del permiso ya existe"
                )
            db_permiso.codigo = permiso_update.codigo
        
        if permiso_update.nombre is not None:
            db_permiso.nombre = permiso_update.nombre
        if permiso_update.descripcion is not None:
            db_permiso.descripcion = permiso_update.descripcion
        if permiso_update.is_active is not None:
            db_permiso.is_active = permiso_update.is_active
        
        db.commit()
        db.refresh(db_permiso)
        return db_permiso

    @staticmethod
    def delete_permiso(db: Session, permiso_id: int) -> bool:
        """Eliminar permiso"""
        db_permiso = PermisoService.get_permiso(db, permiso_id)
        if not db_permiso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permiso no encontrado"
            )
        
        db.delete(db_permiso)
        db.commit()
        return True
