# Sistema de Gestión de Usuarios y Permisos - FastAPI

Aplicación profesional desarrollada con FastAPI que implementa un sistema completo de gestión de usuarios, roles, módulos y permisos con relaciones 1 a N y N a N.

## 🚀 Características

- ✅ **Autenticación JWT** - Sistema de autenticación seguro con tokens
- ✅ **Gestión de Usuarios** - CRUD completo de usuarios
- ✅ **Sistema de Roles** - Asignación de roles a usuarios (1 a N)
- ✅ **Módulos** - Gestión de módulos del sistema (1 a N con usuarios)
- ✅ **Permisos** - Sistema granular de permisos (N a N con roles y módulos)
- ✅ **Variables de Entorno** - Configuración mediante `.env`
- ✅ **Migraciones con Alembic** - Control de versiones de base de datos
- ✅ **Seeders** - Datos iniciales para desarrollo
- ✅ **Middlewares** - Logging, CORS, manejo de errores
- ✅ **Docker Compose** - Despliegue fácil con PostgreSQL
- ✅ **Documentación Automática** - Swagger/OpenAPI en `/docs`

## 📋 Requisitos Previos

- Docker y Docker Compose
- Python 3.11+ (si ejecutas localmente)

## 🛠️ Instalación y Uso

### Con Docker Compose (Recomendado)

1. **Clonar el repositorio** (si aplica)

2. **Configurar variables de entorno**:
   ```bash
   cp .env.example .env
   ```
   Edita `.env` según tus necesidades.

3. **Construir y ejecutar**:
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación**:
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Sin Docker (Desarrollo Local)

1. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar base de datos PostgreSQL**:
   - Crea una base de datos PostgreSQL
   - Actualiza `DATABASE_URL` en `.env`

4. **Ejecutar migraciones**:
   ```bash
   alembic upgrade head
   ```

5. **Ejecutar seeders**:
   ```bash
   python -m app.db.seeders
   ```

6. **Iniciar servidor**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📊 Estructura del Proyecto

```
crud-fastapi/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Endpoints de autenticación
│   │       ├── usuarios.py      # CRUD de usuarios
│   │       ├── roles.py          # CRUD de roles
│   │       ├── modulos.py        # CRUD de módulos
│   │       └── permisos.py       # CRUD de permisos
│   ├── core/
│   │   ├── config.py             # Configuración y variables de entorno
│   │   ├── database.py           # Configuración de SQLAlchemy
│   │   ├── security.py           # JWT y seguridad
│   │   └── middleware.py         # Middlewares personalizados
│   ├── models/                   # Modelos SQLAlchemy
│   │   ├── usuario.py
│   │   ├── rol.py
│   │   ├── modulo.py
│   │   ├── permiso.py
│   │   └── relaciones (N a N)
│   ├── schemas/                  # Schemas Pydantic
│   ├── services/                 # Lógica de negocio
│   └── db/
│       └── seeders.py            # Datos iniciales
├── alembic/                      # Migraciones
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🔐 Usuarios por Defecto

Después de ejecutar los seeders, tendrás estos usuarios:

- **Super Administrador**:
  - Usuario: `admin`
  - Contraseña: `admin123`

- **Usuario Estándar**:
  - Usuario: `user1`
  - Contraseña: `user123`

## 📡 Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Login (form data)
- `POST /api/v1/auth/login/json` - Login (JSON)
- `GET /api/v1/auth/me` - Usuario actual

### Usuarios
- `GET /api/v1/usuarios` - Listar usuarios
- `GET /api/v1/usuarios/{id}` - Obtener usuario
- `POST /api/v1/usuarios` - Crear usuario
- `PUT /api/v1/usuarios/{id}` - Actualizar usuario
- `DELETE /api/v1/usuarios/{id}` - Eliminar usuario
- `POST /api/v1/usuarios/{id}/modulos` - Asignar módulos

### Roles
- `GET /api/v1/roles` - Listar roles
- `GET /api/v1/roles/{id}` - Obtener rol
- `POST /api/v1/roles` - Crear rol
- `PUT /api/v1/roles/{id}` - Actualizar rol
- `DELETE /api/v1/roles/{id}` - Eliminar rol
- `POST /api/v1/roles/{id}/permisos` - Asignar permisos

### Módulos
- `GET /api/v1/modulos` - Listar módulos
- `GET /api/v1/modulos/{id}` - Obtener módulo
- `POST /api/v1/modulos` - Crear módulo
- `PUT /api/v1/modulos/{id}` - Actualizar módulo
- `DELETE /api/v1/modulos/{id}` - Eliminar módulo
- `POST /api/v1/modulos/{id}/permisos` - Asignar permisos

### Permisos
- `GET /api/v1/permisos` - Listar permisos
- `GET /api/v1/permisos/{id}` - Obtener permiso
- `POST /api/v1/permisos` - Crear permiso
- `PUT /api/v1/permisos/{id}` - Actualizar permiso
- `DELETE /api/v1/permisos/{id}` - Eliminar permiso

## 🔗 Relaciones

- **Usuario → Rol**: 1 a N (Un usuario tiene un rol)
- **Usuario → Módulos**: N a N (Un usuario puede tener acceso a múltiples módulos)
- **Rol → Permisos**: N a N (Un rol puede tener múltiples permisos)
- **Módulo → Permisos**: N a N (Un módulo puede requerir múltiples permisos)

## 🧪 Migraciones

### Crear nueva migración:
```bash
alembic revision --autogenerate -m "descripción"
```

### Aplicar migraciones:
```bash
alembic upgrade head
```

### Revertir migración:
```bash
alembic downgrade -1
```

## 🌐 Integración con Frontend

Esta API está lista para ser consumida por cualquier frontend (React, Vue, Angular, etc.). 

### Ejemplo de uso con React:

```javascript
// Login
const response = await fetch('http://localhost:8000/api/v1/auth/login/json', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'admin123' })
});
const { access_token } = await response.json();

// Obtener usuarios (con token)
const users = await fetch('http://localhost:8000/api/v1/usuarios', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```

## 📝 Variables de Entorno

Configura estas variables en tu archivo `.env`:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=crud_fastapi
DATABASE_URL=postgresql://postgres:postgres@db:5432/crud_fastapi

# Security
SECRET_KEY=tu-clave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=True
```

## 🐳 Comandos Docker Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir
docker-compose up --build
```

## 📚 Documentación

Una vez que la aplicación esté corriendo, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
