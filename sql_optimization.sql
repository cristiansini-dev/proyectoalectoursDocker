-- ============================================================================
-- OPTIMIZACIÓN DE BASE DE DATOS - ÍNDICES Y VISTAS
-- ============================================================================

-- ÍNDICES PARA QUERIES DE RESERVAS (90% de uso)
CREATE INDEX IF NOT EXISTS idx_reservas_cliente_id ON reservas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_reservas_hotel_id ON reservas(hotel_id);
CREATE INDEX IF NOT EXISTS idx_reservas_estado ON reservas(estado);
CREATE INDEX IF NOT EXISTS idx_reservas_fecha_inicio ON reservas(fecha_inicio);
CREATE INDEX IF NOT EXISTS idx_reservas_fecha_fin ON reservas(fecha_fin);
CREATE INDEX IF NOT EXISTS idx_reservas_habitacion_id ON reservas(habitacion_id);

-- ÍNDICES PARA QUERIES DE HABITACIONES
CREATE INDEX IF NOT EXISTS idx_habitaciones_hotel_id ON habitaciones(hotel_id);
CREATE INDEX IF NOT EXISTS idx_habitaciones_estado ON habitaciones(estado);
CREATE INDEX IF NOT EXISTS idx_habitaciones_tipo ON habitaciones(tipo);

-- ÍNDICES PARA QUERIES DE PAGOS
CREATE INDEX IF NOT EXISTS idx_pagos_reserva_id ON pagos(reserva_id);
CREATE INDEX IF NOT EXISTS idx_pagos_cliente_id ON pagos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_pagos_estado ON pagos(estado);
CREATE INDEX IF NOT EXISTS idx_pagos_fecha_pago ON pagos(fecha_pago);
CREATE INDEX IF NOT EXISTS idx_pagos_metodo ON pagos(metodo_pago);

-- ÍNDICES PARA QUERIES DE CLIENTES
CREATE INDEX IF NOT EXISTS idx_clientes_correo ON clientes(correo);
CREATE INDEX IF NOT EXISTS idx_clientes_telefono ON clientes(telefono);
CREATE INDEX IF NOT EXISTS idx_clientes_fecha_registro ON clientes(fecha_registro);

-- ÍNDICES PARA QUERIES DE PAQUETES
CREATE INDEX IF NOT EXISTS idx_paquetes_nombre ON paquetes(nombre);
CREATE INDEX IF NOT EXISTS idx_paquetes_estado ON paquetes(estado);

-- ÍNDICES PARA QUERIES DE EMPLEADOS
CREATE INDEX IF NOT EXISTS idx_empleados_hotel_id ON empleados(hotel_id);
CREATE INDEX IF NOT EXISTS idx_empleados_cargo ON empleados(cargo);

-- ÍNDICES COMPUESTOS PARA QUERIES COMPLEJAS
CREATE INDEX IF NOT EXISTS idx_reservas_hotel_fecha ON reservas(hotel_id, fecha_inicio, fecha_fin);
CREATE INDEX IF NOT EXISTS idx_habitaciones_hotel_estado ON habitaciones(hotel_id, estado);
CREATE INDEX IF NOT EXISTS idx_pagos_reserva_estado ON pagos(reserva_id, estado);

-- ============================================================================
-- VISTAS PARA REPORTES Y DASHBOARDS (Reducen lógica en Python)
-- ============================================================================

-- VISTA: Ocupación por Hotel (usada en dashboard)
CREATE VIEW IF NOT EXISTS v_ocupacion_por_hotel AS
SELECT 
    h.id_hotel,
    h.nombre,
    COUNT(hab.id_habitacion) as total_habitaciones,
    SUM(CASE WHEN hab.estado = 'ocupada' THEN 1 ELSE 0 END) as ocupadas,
    ROUND(
        (SUM(CASE WHEN hab.estado = 'ocupada' THEN 1 ELSE 0 END) * 100.0) / 
        COUNT(hab.id_habitacion),
        2
    ) as porcentaje_ocupacion,
    COUNT(hab.id_habitacion) - SUM(CASE WHEN hab.estado = 'ocupada' THEN 1 ELSE 0 END) as disponibles
FROM hoteles h
LEFT JOIN habitaciones hab ON h.id_hotel = hab.hotel_id
GROUP BY h.id_hotel, h.nombre;

-- VISTA: Ingresos por mes
CREATE VIEW IF NOT EXISTS v_ingresos_mensuales AS
SELECT 
    DATE_TRUNC('month', p.fecha_pago)::date as mes,
    COUNT(*) as total_pagos,
    SUM(p.monto) as total_ingresos,
    AVG(p.monto) as promedio_pago,
    MIN(p.monto) as pago_minimo,
    MAX(p.monto) as pago_maximo
FROM pagos p
WHERE p.estado = 'completado'
GROUP BY DATE_TRUNC('month', p.fecha_pago);

-- VISTA: Estadísticas de reservas
CREATE VIEW IF NOT EXISTS v_estadisticas_reservas AS
SELECT 
    r.estado,
    COUNT(*) as total_reservas,
    SUM(r.total_costo) as ingresos_totales,
    AVG(r.total_costo) as promedio_reserva,
    AVG(EXTRACT(DAY FROM (r.fecha_fin - r.fecha_inicio))) as dias_promedio,
    MIN(r.fecha_inicio) as primera_reserva,
    MAX(r.fecha_inicio) as ultima_reserva
FROM reservas r
GROUP BY r.estado;

-- VISTA: Top paquetes vendidos
CREATE VIEW IF NOT EXISTS v_top_paquetes AS
SELECT 
    p.id_paquete,
    p.nombre,
    p.precio,
    COUNT(r.id_reserva) as veces_vendido,
    SUM(r.total_costo) as ingresos,
    ROUND(AVG(r.total_costo), 2) as promedio_venta
FROM paquetes p
LEFT JOIN reservas r ON p.id_paquete = r.paquete_id AND r.estado = 'confirmada'
GROUP BY p.id_paquete, p.nombre, p.precio
ORDER BY veces_vendido DESC;

-- VISTA: Actividad de clientes (últimas 30 días)
CREATE VIEW IF NOT EXISTS v_actividad_clientes AS
SELECT 
    c.id_cliente,
    c.nombre,
    c.apellido,
    c.correo,
    COUNT(r.id_reserva) as total_reservas,
    SUM(r.total_costo) as gasto_total,
    MAX(r.fecha_inicio) as ultima_reserva,
    CASE 
        WHEN MAX(r.fecha_inicio) >= CURRENT_DATE - INTERVAL 30 DAY THEN 'activo'
        ELSE 'inactivo'
    END as estado_cliente
FROM clientes c
LEFT JOIN reservas r ON c.id_cliente = r.cliente_id
GROUP BY c.id_cliente, c.nombre, c.apellido, c.correo;

-- VISTA: Empleados por hotel
CREATE VIEW IF NOT EXISTS v_empleados_por_hotel AS
SELECT 
    h.id_hotel,
    h.nombre as hotel_nombre,
    COUNT(e.id_empleado) as total_empleados,
    SUM(CASE WHEN e.cargo = 'gerente' THEN 1 ELSE 0 END) as gerentes,
    SUM(CASE WHEN e.cargo = 'recepcionista' THEN 1 ELSE 0 END) as recepcionistas,
    SUM(CASE WHEN e.cargo = 'limpieza' THEN 1 ELSE 0 END) as limpieza,
    SUM(CASE WHEN e.cargo = 'otros' THEN 1 ELSE 0 END) as otros
FROM hoteles h
LEFT JOIN empleados e ON h.id_hotel = e.hotel_id
GROUP BY h.id_hotel, h.nombre;

-- VISTA: Predicción de ingresos (próximos 30 días)
CREATE VIEW IF NOT EXISTS v_ingresos_proximos_30_dias AS
SELECT 
    DATE(r.fecha_inicio) as fecha,
    h.nombre as hotel,
    COUNT(*) as total_reservas,
    SUM(r.total_costo) as ingresos_estimados
FROM reservas r
JOIN hoteles h ON r.hotel_id = h.id_hotel
WHERE r.fecha_inicio >= CURRENT_DATE 
    AND r.fecha_inicio <= CURRENT_DATE + INTERVAL 30 DAY
    AND r.estado IN ('confirmada', 'pendiente')
GROUP BY DATE(r.fecha_inicio), h.nombre
ORDER BY fecha DESC;

-- ============================================================================
-- QUERIES OPTIMIZADAS COMÚNMENTE USADAS
-- ============================================================================

-- QUERY: Obtener habitaciones disponibles por fecha
-- ANTES: O(n^2) sin índices → DESPUÉS: O(log n) con índices
SELECT 
    h.id_habitacion,
    h.numero_habitacion,
    h.tipo,
    h.precio_noche,
    hot.nombre as hotel_nombre
FROM habitaciones h
JOIN hoteles hot ON h.hotel_id = hot.id_hotel
WHERE h.estado = 'disponible'
    AND h.hotel_id = ?
    AND h.id_habitacion NOT IN (
        SELECT habitacion_id FROM reservas 
        WHERE estado = 'confirmada'
            AND (
                (fecha_inicio <= ? AND fecha_fin >= ?)
                OR (fecha_inicio <= ? AND fecha_fin >= ?)
            )
    )
ORDER BY h.precio_noche ASC;

-- QUERY: Obtener ingresos por periodo
SELECT 
    DATE_TRUNC('day', p.fecha_pago)::date as fecha,
    COUNT(*) as transacciones,
    SUM(p.monto) as total_ingresos,
    COUNT(DISTINCT p.cliente_id) as clientes_unicos
FROM pagos p
WHERE p.estado = 'completado'
    AND p.fecha_pago >= ?
    AND p.fecha_pago <= ?
GROUP BY DATE_TRUNC('day', p.fecha_pago)
ORDER BY fecha DESC;

-- QUERY: Reservas por cliente en detalle
SELECT 
    r.id_reserva,
    r.fecha_inicio,
    r.fecha_fin,
    h.nombre as hotel,
    hab.numero_habitacion,
    hab.tipo,
    r.total_costo,
    r.estado,
    p.id_paquete,
    p.nombre as paquete_nombre
FROM reservas r
JOIN hoteles h ON r.hotel_id = h.id_hotel
JOIN habitaciones hab ON r.habitacion_id = hab.id_habitacion
LEFT JOIN paquetes p ON r.paquete_id = p.id_paquete
WHERE r.cliente_id = ?
ORDER BY r.fecha_inicio DESC;

-- QUERY: Estadísticas de ocupación por mes
SELECT 
    DATE_TRUNC('month', r.fecha_inicio)::date as mes,
    h.nombre as hotel,
    COUNT(DISTINCT r.id_reserva) as reservas,
    AVG(EXTRACT(DAY FROM (r.fecha_fin - r.fecha_inicio))) as dias_promedio,
    SUM(r.total_costo) as ingresos_mes,
    COUNT(DISTINCT r.cliente_id) as clientes_unicos
FROM reservas r
JOIN hoteles h ON r.hotel_id = h.id_hotel
WHERE r.estado = 'confirmada'
GROUP BY DATE_TRUNC('month', r.fecha_inicio), h.nombre
ORDER BY mes DESC;

-- ============================================================================
-- ESTADÍSTICAS DE ÍNDICES (ejecutar periódicamente)
-- ============================================================================

-- Para analizar uso de índices:
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Para encontrar índices no usados:
SELECT schemaname, tablename, indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY tablename, indexname;

-- Para VACUUM y ANALYZE
VACUUM ANALYZE;
