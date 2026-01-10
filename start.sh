#!/bin/bash

echo "🚀 Iniciando Sistema de Gestión de Usuarios y Permisos..."
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instálalo primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instálalo primero."
    exit 1
fi

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "✓ Archivo .env creado. Por favor revisa y ajusta las variables si es necesario."
fi

# Construir y levantar los servicios
echo "🐳 Construyendo y levantando contenedores Docker..."
docker-compose up --build -d

echo ""
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

echo ""
echo "✅ Servicios iniciados!"
echo ""
echo "📍 URLs importantes:"
echo "   - API: http://localhost:8000"
echo "   - Documentación Swagger: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "🔐 Usuarios por defecto:"
echo "   - Usuario: admin / Contraseña: admin123"
echo "   - Usuario: user1 / Contraseña: user123"
echo ""
echo "📊 Ver logs: docker-compose logs -f"
echo "🛑 Detener servicios: docker-compose down"
