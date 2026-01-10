from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.rol import Rol
from app.models.rol_permiso import RolPermiso
from app.schemas.rol import RolCreate, RolUpdate


class RolService:
    @staticmethod
    def get_rol(db: Session, rol_id: int) -> Optional[Rol]:
        """Obtener rol por ID"""
        return db.query(Rol).filter(Rol.id == rol_id).first()

    @staticmethod
    def get_rol_by_nombre(db: Session, nombre: str) -> Optional[Rol]:
        """Obtener rol por nombre"""
        return db.query(Rol).filter(Rol.nombre == nombre).first()

    @staticmethod
    def get_roles(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[Rol]:
        """Obtener lista de roles"""
        query = db.query(Rol)
        if is_active is not None:
            query = query.filter(Rol.is_active == is_active)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_rol(db: Session, rol: RolCreate) -> Rol:
        """Crear nuevo rol"""
        if RolService.get_rol_by_nombre(db, rol.nombre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del rol ya existe"
            )
        
        db_rol = Rol(
            nombre=rol.nombre,
            descripcion=rol.descripcion,
            is_active=rol.is_active
        )
        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        
        # Asignar permisos
        if rol.permiso_ids:
            RolService.asignar_permisos(db, db_rol.id, rol.permiso_ids)
            db.refresh(db_rol)
        
        return db_rol

    @staticmethod
    def update_rol(db: Session, rol_id: int, rol_update: RolUpdate) -> Rol:
        """Actualizar rol"""
        db_rol = RolService.get_rol(db, rol_id)
        if not db_rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        if rol_update.nombre and rol_update.nombre != db_rol.nombre:
            if RolService.get_rol_by_nombre(db, rol_update.nombre):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre del rol ya existe"
                )
            db_rol.nombre = rol_update.nombre
        
        if rol_update.descripcion is not None:
            db_rol.descripcion = rol_update.descripcion
        if rol_update.is_active is not None:
            db_rol.is_active = rol_update.is_active
        
        if rol_update.permiso_ids is not None:
            RolService.asignar_permisos(db, rol_id, rol_update.permiso_ids)
        
        db.commit()
        db.refresh(db_rol)
        return db_rol

    @staticmethod
    def delete_rol(db: Session, rol_id: int) -> bool:
        """Eliminar rol"""
        db_rol = RolService.get_rol(db, rol_id)
        if not db_rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        db.delete(db_rol)
        db.commit()
        return True

    @staticmethod
    def asignar_permisos(db: Session, rol_id: int, permiso_ids: List[int]) -> Rol:
        """Asignar permisos a rol"""
        db_rol = RolService.get_rol(db, rol_id)
        if not db_rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        # Eliminar asignaciones existentes
        db.query(RolPermiso).filter(RolPermiso.rol_id == rol_id).delete()
        
        # Crear nuevas asignaciones
        for permiso_id in permiso_ids:
            rol_permiso = RolPermiso(
                rol_id=rol_id,
                permiso_id=permiso_id,
                is_active=True
            )
            db.add(rol_permiso)
        
        db.commit()
        db.refresh(db_rol)
        return db_rol
