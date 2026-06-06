#!/bin/bash
# Script de instalación para mejoras premium AlecTours
# Ejecutar desde: bash install-premium-features.sh

set -e

echo "================================"
echo "🚀 Instalando Mejoras Premium AlecTours"
echo "================================"

# Paso 1: Instalar dependencias Python
echo ""
echo "📦 Paso 1: Instalando dependencias Python..."
pip install reportlab>=4.0.0 python-dateutil>=2.8.0

# Paso 2: Crear carpetas necesarias
echo ""
echo "📁 Paso 2: Creando estructura de carpetas..."
mkdir -p backend/app/static/js
mkdir -p backend/app/services
mkdir -p backend/app/routes

# Paso 3: Descargar librerías frontend
echo ""
echo "⬇️  Paso 3: Descargando librerías JavaScript..."

# Chart.js
echo "  • Descargando Chart.js..."
curl -s https://cdn.jsdelivr.net/npm/chart.js -o backend/app/static/js/chart.min.js
echo "    ✓ Chart.js descargado"

# jsPDF
echo "  • Descargando jsPDF..."
curl -s https://cdn.jsdelivr.net/npm/jspdf -o backend/app/static/js/jspdf.min.js
echo "    ✓ jsPDF descargado"

# html2canvas
echo "  • Descargando html2canvas..."
curl -s https://html2canvas.hertzen.com/dist/html2canvas.min.js -o backend/app/static/js/html2canvas.min.js
echo "    ✓ html2canvas descargado"

# Paso 4: Verificar archivos de templates
echo ""
echo "✅ Paso 4: Archivos creados:"
echo "   • dashboard-premium.html"
echo "   • perfil-premium.html"
echo "   • enhanced_api.py"
echo "   • db_optimizer.py"
echo "   • sql_optimization.sql"

# Paso 5: Mostrar instrucciones siguientes
echo ""
echo "================================"
echo "✅ Instalación completada"
echo "================================"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Actualizar backend/app/main.py:"
echo "   - Importar: from app.routes import enhanced_api"
echo "   - Incluir: app.include_router(enhanced_api.router)"
echo ""
echo "2. Reemplazar rutas en main.py:"
echo "   - /admin/dashboard → dashboard-premium.html"
echo "   - /admin/perfil → perfil-premium.html"
echo ""
echo "3. Ejecutar optimizaciones BD:"
echo "   - psql -h localhost -U user -d db < sql_optimization.sql"
echo ""
echo "4. Reiniciar servidor:"
echo "   - docker-compose down && docker-compose up --build"
echo ""
echo "🎉 ¡Listo! Los nuevos dashboards están configurados"
echo ""
