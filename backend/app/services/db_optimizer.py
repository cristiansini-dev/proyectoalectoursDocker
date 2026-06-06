"""
Script para ejecutar optimizaciones de BD directamente desde FastAPI
Guardar en: backend/app/services/db_optimizer.py
"""

from sqlalchemy import text
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def create_indexes(db: Session):
    """Crea todos los índices de optimización automáticamente"""
    
    indexes = [
        # ÍNDICES PARA RESERVAS
        "CREATE INDEX IF NOT EXISTS idx_reservas_cliente_id ON reservas(cliente_id);",
        "CREATE INDEX IF NOT EXISTS idx_reservas_hotel_id ON reservas(hotel_id);",
        "CREATE INDEX IF NOT EXISTS idx_reservas_estado ON reservas(estado);",
        "CREATE INDEX IF NOT EXISTS idx_reservas_fecha_inicio ON reservas(fecha_inicio);",
        "CREATE INDEX IF NOT EXISTS idx_reservas_fecha_fin ON reservas(fecha_fin);",
        "CREATE INDEX IF NOT EXISTS idx_reservas_habitacion_id ON reservas(habitacion_id);",
        
        # ÍNDICES PARA HABITACIONES
        "CREATE INDEX IF NOT EXISTS idx_habitaciones_hotel_id ON habitaciones(hotel_id);",
        "CREATE INDEX IF NOT EXISTS idx_habitaciones_estado ON habitaciones(estado);",
        "CREATE INDEX IF NOT EXISTS idx_habitaciones_tipo ON habitaciones(tipo);",
        
        # ÍNDICES PARA PAGOS
        "CREATE INDEX IF NOT EXISTS idx_pagos_reserva_id ON pagos(reserva_id);",
        "CREATE INDEX IF NOT EXISTS idx_pagos_cliente_id ON pagos(cliente_id);",
        "CREATE INDEX IF NOT EXISTS idx_pagos_estado ON pagos(estado);",
        "CREATE INDEX IF NOT EXISTS idx_pagos_fecha_pago ON pagos(fecha_pago);",
        "CREATE INDEX IF NOT EXISTS idx_pagos_metodo ON pagos(metodo_pago);",
        
        # ÍNDICES PARA CLIENTES
        "CREATE INDEX IF NOT EXISTS idx_clientes_correo ON clientes(correo);",
        "CREATE INDEX IF NOT EXISTS idx_clientes_telefono ON clientes(telefono);",
        "CREATE INDEX IF NOT EXISTS idx_clientes_fecha_registro ON clientes(fecha_registro);",
        
        # ÍNDICES PARA PAQUETES
        "CREATE INDEX IF NOT EXISTS idx_paquetes_nombre ON paquetes(nombre);",
        "CREATE INDEX IF NOT EXISTS idx_paquetes_estado ON paquetes(estado);",
        
        # ÍNDICES PARA EMPLEADOS
        "CREATE INDEX IF NOT EXISTS idx_empleados_hotel_id ON empleados(hotel_id);",
        "CREATE INDEX IF NOT EXISTS idx_empleados_cargo ON empleados(cargo);",
        
        # ÍNDICES COMPUESTOS
        "CREATE INDEX IF NOT EXISTS idx_reservas_hotel_fecha ON reservas(hotel_id, fecha_inicio, fecha_fin);",
        "CREATE INDEX IF NOT EXISTS idx_habitaciones_hotel_estado ON habitaciones(hotel_id, estado);",
        "CREATE INDEX IF NOT EXISTS idx_pagos_reserva_estado ON pagos(reserva_id, estado);",
    ]
    
    success_count = 0
    error_count = 0
    
    for index_sql in indexes:
        try:
            db.execute(text(index_sql))
            success_count += 1
            logger.info(f"✓ Índice creado: {index_sql.split('ON')[1].split('(')[0].strip()}")
        except Exception as e:
            error_count += 1
            logger.warning(f"⚠ {str(e)[:100]}")
    
    db.commit()
    logger.info(f"✓ Índices: {success_count} creados, {error_count} errores/existentes")
    
    return {"indexes_created": success_count, "errors": error_count}


def create_views(db: Session):
    """Crea vistas para reportes y dashboards"""
    
    views = {
        "v_ocupacion_por_hotel": """
            SELECT 
                h.id_hotel,
                h.nombre,
                COUNT(hab.id_habitacion) as total_habitaciones,
                SUM(CASE WHEN hab.estado = 'ocupada' THEN 1 ELSE 0 END) as ocupadas,
                ROUND(
                    (SUM(CASE WHEN hab.estado = 'ocupada' THEN 1 ELSE 0 END) * 100.0) / 
                    NULLIF(COUNT(hab.id_habitacion), 0),
                    2
                ) as porcentaje_ocupacion,
                COUNT(hab.id_habitacion) - SUM(CASE WHEN hab.estado = 'ocupada' THEN 1 ELSE 0 END) as disponibles
            FROM hoteles h
            LEFT JOIN habitaciones hab ON h.id_hotel = hab.hotel_id
            GROUP BY h.id_hotel, h.nombre
        """,
        
        "v_estadisticas_reservas": """
            SELECT 
                r.estado,
                COUNT(*) as total_reservas,
                SUM(r.total_costo) as ingresos_totales,
                AVG(r.total_costo) as promedio_reserva,
                MIN(r.fecha_inicio) as primera_reserva,
                MAX(r.fecha_inicio) as ultima_reserva
            FROM reservas r
            GROUP BY r.estado
        """,
        
        "v_top_paquetes": """
            SELECT 
                p.id_paquete,
                p.nombre,
                p.precio,
                COUNT(r.id_reserva) as veces_vendido,
                SUM(r.total_costo) as ingresos
            FROM paquetes p
            LEFT JOIN reservas r ON p.id_paquete = r.paquete_id AND r.estado = 'confirmada'
            GROUP BY p.id_paquete, p.nombre, p.precio
            ORDER BY veces_vendido DESC
        """,
        
        "v_actividad_clientes": """
            SELECT 
                c.id_cliente,
                c.nombre,
                c.apellido,
                c.correo,
                COUNT(r.id_reserva) as total_reservas,
                SUM(r.total_costo) as gasto_total,
                MAX(r.fecha_inicio) as ultima_reserva
            FROM clientes c
            LEFT JOIN reservas r ON c.id_cliente = r.cliente_id
            GROUP BY c.id_cliente, c.nombre, c.apellido, c.correo
        """
    }
    
    success_count = 0
    
    for view_name, view_sql in views.items():
        try:
            drop_sql = f"DROP VIEW IF EXISTS {view_name};"
            db.execute(text(drop_sql))
            
            create_sql = f"CREATE VIEW {view_name} AS {view_sql};"
            db.execute(text(create_sql))
            
            success_count += 1
            logger.info(f"✓ Vista creada: {view_name}")
        except Exception as e:
            logger.warning(f"⚠ Error en vista {view_name}: {str(e)[:100]}")
    
    db.commit()
    logger.info(f"✓ Vistas: {success_count} creadas")
    
    return {"views_created": success_count}


def optimize_database(db: Session):
    """Ejecuta todas las optimizaciones"""
    
    logger.info("🚀 Iniciando optimizaciones de BD...")
    
    try:
        # Crear índices
        indexes_result = create_indexes(db)
        
        # Crear vistas
        views_result = create_views(db)
        
        # Ejecutar VACUUM y ANALYZE (solo en PostgreSQL)
        try:
            # Nota: VACUUM no es soportado en transacciones, se ejecuta con autocommit
            db.commit()
            db.execute(text("VACUUM ANALYZE;"))
            logger.info("✓ VACUUM ANALYZE ejecutado")
        except Exception as e:
            logger.warning(f"⚠ VACUUM ANALYZE no disponible: {str(e)[:50]}")
        
        logger.info("✅ Optimizaciones completadas")
        
        return {
            "status": "success",
            "indexes": indexes_result,
            "views": views_result
        }
    
    except Exception as e:
        logger.error(f"❌ Error en optimizaciones: {str(e)}")
        return {"status": "error", "error": str(e)}


# Función para ejecutar en startup
async def init_database_optimizations(db: Session):
    """Se ejecuta al iniciar la aplicación"""
    try:
        optimize_database(db)
    except Exception as e:
        logger.warning(f"No se pudieron ejecutar optimizaciones al inicio: {e}")
