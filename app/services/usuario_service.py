from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.usuario import Usuario
from app.models.usuario_rol import UsuarioRol
from app.models.rol_modulo import RolModulo
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash
from datetime import datetime


class UsuarioService:
    @staticmethod
    def get_usuario(db: Session, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    @staticmethod
    def get_usuario_by_username(db: Session, username: str) -> Optional[Usuario]:
        """Obtener usuario por username"""
        return db.query(Usuario).filter(Usuario.username == username).first()

    @staticmethod
    def get_usuario_by_email(db: Session, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()

    @staticmethod
    def get_usuarios(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Usuario]:
        """Obtener lista de usuarios con paginación y búsqueda"""
        query = db.query(Usuario)
        
        if search:
            query = query.filter(
                or_(
                    Usuario.username.ilike(f"%{search}%"),
                    Usuario.email.ilike(f"%{search}%"),
                    Usuario.nombre_completo.ilike(f"%{search}%")
                )
            )
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
        """Crear nuevo usuario"""
        # Verificar si username existe
        if UsuarioService.get_usuario_by_username(db, usuario.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está en uso"
            )
        
        # Verificar si email existe
        if UsuarioService.get_usuario_by_email(db, usuario.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso"
            )
        
        # Crear usuario
        db_usuario = Usuario(
            username=usuario.username,
            email=usuario.email,
            nombre_completo=usuario.nombre_completo,
            hashed_password=get_password_hash(usuario.password),
            is_active=usuario.is_active
        )
        
        db.add(db_usuario)
        db.flush()
        
        # Asignar roles si se proporcionan
        if usuario.rol_ids:
            for rol_id in usuario.rol_ids:
                usuario_rol = UsuarioRol(
                    usuario_id=db_usuario.id,
                    rol_id=rol_id,
                    is_active=True
                )
                db.add(usuario_rol)
        
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def update_usuario(
        db: Session,
        usuario_id: int,
        usuario_update: UsuarioUpdate
    ) -> Usuario:
        """Actualizar usuario"""
        db_usuario = UsuarioService.get_usuario(db, usuario_id)
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar username único
        if usuario_update.username and usuario_update.username != db_usuario.username:
            if UsuarioService.get_usuario_by_username(db, usuario_update.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El username ya está en uso"
                )
            db_usuario.username = usuario_update.username
        
        # Verificar email único
        if usuario_update.email and usuario_update.email != db_usuario.email:
            if UsuarioService.get_usuario_by_email(db, usuario_update.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está en uso"
                )
            db_usuario.email = usuario_update.email
        
        # Actualizar otros campos
        if usuario_update.nombre_completo is not None:
            db_usuario.nombre_completo = usuario_update.nombre_completo
        if usuario_update.password is not None:
            db_usuario.hashed_password = get_password_hash(usuario_update.password)
        if usuario_update.is_active is not None:
            db_usuario.is_active = usuario_update.is_active
        
        # Actualizar roles si se proporcionan
        if usuario_update.rol_ids is not None:
            UsuarioService.asignar_roles(db, usuario_id, usuario_update.rol_ids)
        
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def delete_usuario(db: Session, usuario_id: int) -> bool:
        """Eliminar usuario"""
        db_usuario = UsuarioService.get_usuario(db, usuario_id)
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        db.delete(db_usuario)
        db.commit()
        return True

    @staticmethod
    def asignar_roles(
        db: Session,
        usuario_id: int,
        rol_ids: List[int]
    ) -> Usuario:
        """Asignar roles a usuario"""
        db_usuario = UsuarioService.get_usuario(db, usuario_id)
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Eliminar asignaciones existentes
        db.query(UsuarioRol).filter(UsuarioRol.usuario_id == usuario_id).delete()
        
        # Crear nuevas asignaciones
        for rol_id in rol_ids:
            usuario_rol = UsuarioRol(
                usuario_id=usuario_id,
                rol_id=rol_id,
                is_active=True
            )
            db.add(usuario_rol)
        
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def get_modulos_from_roles(db: Session, usuario_id: int) -> List:
        """
        Obtener módulos del usuario calculados desde sus roles.
        Si un módulo está en múltiples roles, se incluye una sola vez.
        """
        from app.models.modulo import Modulo
        
        db_usuario = UsuarioService.get_usuario(db, usuario_id)
        if not db_usuario:
            return []
        
        # Obtener todos los módulos de los roles activos del usuario
        modulos_ids = set()
        modulos_list = []
        
        for usuario_rol in db_usuario.roles:
            if usuario_rol.is_active and usuario_rol.rol.is_active:
                for rol_modulo in usuario_rol.rol.modulos:
                    if rol_modulo.is_active and rol_modulo.modulo.is_active:
                        if rol_modulo.modulo_id not in modulos_ids:
                            modulos_ids.add(rol_modulo.modulo_id)
                            modulos_list.append(rol_modulo.modulo)
        
        return modulos_list

    @staticmethod
    def update_last_login(db: Session, usuario: Usuario):
        """Actualizar último login"""
        usuario.last_login = datetime.utcnow()
        db.commit()
        db.refresh(usuario)
