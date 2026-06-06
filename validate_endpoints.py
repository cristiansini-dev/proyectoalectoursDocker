#!/usr/bin/env python3
"""
Script de validación de endpoints
Ejecutar desde: python validate_endpoints.py
"""

import sys
import os

def check_file(path, description):
    """Verifica que un archivo exista"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_import(module_path, description):
    """Verifica que un módulo se pueda importar"""
    try:
        parts = module_path.split('.')
        module = __import__(module_path)
        for part in parts[1:]:
            module = getattr(module, part)
        print(f"✅ Importable: {description}")
        return True
    except Exception as e:
        print(f"❌ Error importando {description}: {str(e)[:80]}")
        return False

def main():
    print("=" * 60)
    print("🔍 VALIDANDO ENDPOINTS CORREGIDOS")
    print("=" * 60)
    print()
    
    # 1. Verificar archivos
    print("📁 Archivos Necesarios:")
    files_ok = True
    files_ok &= check_file("backend/app/routes/enhanced_api.py", "API Endpoints")
    files_ok &= check_file("backend/app/main.py", "Main FastAPI")
    files_ok &= check_file("backend/app/templates/admin/dashboard-premium.html", "Dashboard Premium")
    files_ok &= check_file("backend/app/templates/admin/perfil-premium.html", "Perfil Premium")
    print()
    
    # 2. Verificar modelos
    print("📦 Modelos ORM:")
    models_ok = True
    models_ok &= check_import("app.models.reserva_model.Reserva", "Reserva Model")
    models_ok &= check_import("app.models.cliente_model.Cliente", "Cliente Model")
    models_ok &= check_import("app.models.reserva_model.Paquete", "Paquete Model")
    models_ok &= check_import("app.models.hotel_model.Hotel", "Hotel Model")
    print()
    
    # 3. Verificar dependencias
    print("📚 Dependencias Python:")
    deps_ok = True
    try:
        import reportlab
        print("✅ reportlab instalado")
    except:
        print("❌ reportlab NO instalado (pip install reportlab)")
        deps_ok = False
    
    try:
        import fastapi
        print("✅ fastapi instalado")
    except:
        print("❌ fastapi NO instalado")
        deps_ok = False
    
    try:
        import sqlalchemy
        print("✅ sqlalchemy instalado")
    except:
        print("❌ sqlalchemy NO instalado")
        deps_ok = False
    
    print()
    
    # Resumen
    print("=" * 60)
    if files_ok and models_ok and deps_ok:
        print("✅ VALIDACIÓN EXITOSA - Todo está configurado correctamente")
        print()
        print("📌 Próximos pasos:")
        print("  1. docker-compose down && docker-compose up --build")
        print("  2. Visitar http://localhost:8000/docs para ver todos los endpoints")
        print("  3. Testear /api/dashboard/stats")
        return 0
    else:
        print("❌ VALIDACIÓN FALLIDA - Corrige los errores anteriores")
        print()
        if not files_ok:
            print("  • Verifica que los archivos estén en el lugar correcto")
        if not models_ok:
            print("  • Verifica que los modelos estén correctamente importados")
        if not deps_ok:
            print("  • Instala dependencias faltantes con: pip install reportlab")
        return 1

if __name__ == "__main__":
    sys.exit(main())
