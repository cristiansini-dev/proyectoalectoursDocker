# GUÍA DE INTEGRACIÓN - Mejoras Premium AlecTours

## 1. INSTALACIÓN DE DEPENDENCIAS

```bash
# Frontend - agregar CDNs a base.html (si no existen)
# Chart.js para gráficas
# <script src="/static/js/chart.min.js"></script>

# PDF generation
# <script src="/static/js/jspdf.min.js"></script>
# <script src="/static/js/html2canvas.min.js"></script>

# Backend - pip
pip install reportlab>=4.0.0
pip install python-dateutil>=2.8.0
```

## 2. ARCHIVOS NUEVOS CREADOS

```
backend/
  app/
    routes/
      enhanced_api.py ← Nuevos endpoints para dashboard, PDFs, perfil
    templates/
      admin/
        dashboard-premium.html ← Dashboard con gráficas
        perfil-premium.html ← Perfil usuario con historial

sql_optimization.sql ← Índices y vistas de BD
SETUP.md ← Este archivo
```

## 3. ACTUALIZAR main.py

En `backend/app/main.py`, agregar:

```python
from app.routes import enhanced_api

app.include_router(enhanced_api.router)
```

## 4. REEMPLAZAR RUTAS EXISTENTES

En `backend/app/main.py`:

```python
# REEMPLAZAR
@app.get("/admin/dashboard")
def dashboard(...):
    return templates.TemplateResponse("admin/dashboard.html", ...)

# CON
@app.get("/admin/dashboard")
def dashboard(...):
    return templates.TemplateResponse("admin/dashboard-premium.html", ...)

# REEMPLAZAR
@app.get("/admin/perfil")
def perfil(...):
    return templates.TemplateResponse("admin/perfil.html", ...)

# CON
@app.get("/admin/perfil")
def perfil(...):
    return templates.TemplateResponse("admin/perfil-premium.html", ...)
```

## 5. EJECUTAR OPTIMIZACIONES DE BD

```bash
# Conectar a PostgreSQL
psql -h localhost -U alectours_user -d alectours_db < sql_optimization.sql

# O ejecutar statements individuales en PgAdmin
```

## 6. ESTRUCTURA DE RESPUESTAS API

```javascript
// Dashboard Stats
GET /api/dashboard/stats
{
  "ingresos_totales": 50000.00,
  "ingresos_mes": 12000.00,
  "reservas_confirmadas": 45,
  "ocupacion_promedio": 78.5,
  "clientes_nuevos": 12,
  "habitaciones_disponibles": 22
}

// Ingresos Mensuales
GET /api/dashboard/ingresos-mensuales?meses=6
[
  {"mes": "Jun 24", "ingresos": 5000.00},
  {"mes": "May 24", "ingresos": 4800.00},
  ...
]

// Ocupación por Hotel
GET /api/dashboard/ocupacion-hoteles
[
  {"hotel": "Hotel Paradise", "ocupacion": 85.5, "ocupadas": 17, "total": 20},
  ...
]

// Top Paquetes
GET /api/dashboard/top-paquetes?limit=5
[
  {
    "id": 1,
    "nombre": "Caribbean Dreams",
    "precio": 2500.00,
    "veces_vendido": 15,
    "ingresos_totales": 37500.00
  },
  ...
]
```

## 7. DESCARGAR LIBRERÍAS FRONTEND

Crear carpeta `backend/app/static/js/` y descargar:

```bash
# Chart.js
curl https://cdn.jsdelivr.net/npm/chart.js -o backend/app/static/js/chart.min.js

# jsPDF
curl https://cdn.jsdelivr.net/npm/jspdf -o backend/app/static/js/jspdf.min.js

# html2canvas
curl https://html2canvas.hertzen.com/dist/html2canvas.min.js -o backend/app/static/js/html2canvas.min.js
```

## 8. SCHEMA DE BD RECOMENDADO

Las vistas SQL requieren estas columnas (verificar que existan):

```sql
-- Tabla Reservas
id_reserva INT PRIMARY KEY
cliente_id INT FOREIGN KEY
hotel_id INT FOREIGN KEY
habitacion_id INT FOREIGN KEY
paquete_id INT FOREIGN KEY
fecha_inicio DATE
fecha_fin DATE
total_costo DECIMAL
estado VARCHAR (confirmada/pendiente/cancelada/completada)

-- Tabla Habitaciones
id_habitacion INT PRIMARY KEY
hotel_id INT FOREIGN KEY
numero_habitacion VARCHAR
tipo VARCHAR
estado VARCHAR (ocupada/disponible/mantenimiento)
precio_noche DECIMAL

-- Tabla Clientes
id_cliente INT PRIMARY KEY
nombre VARCHAR
apellido VARCHAR
correo VARCHAR
telefono VARCHAR
pais VARCHAR
fecha_registro TIMESTAMP

-- Tabla Pagos
id_pago INT PRIMARY KEY
reserva_id INT FOREIGN KEY
cliente_id INT FOREIGN KEY
monto DECIMAL
fecha_pago TIMESTAMP
metodo_pago VARCHAR
estado VARCHAR (completado/pendiente/fallido)
```

## 9. FUNCIONES fetchAPI REQUERIDAS

En `backend/app/templates/layouts/base.html`, asegúrate que exista:

```javascript
async function fetchAPI(method, url, data) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    };

    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        const result = await response.json();
        return {
            ok: response.ok,
            data: result
        };
    } catch (error) {
        console.error('API Error:', error);
        return {
            ok: false,
            data: null,
            error: error.message
        };
    }
}

function showSuccess(message) {
    // Mostrar notificación de éxito
    alert(message);
}

function showError(message) {
    // Mostrar notificación de error
    alert('Error: ' + message);
}

function showConfirm(message) {
    return confirm(message);
}
```

## 10. MEJORAS FUTURAS RECOMENDADAS

- [ ] Sistema de cache con Redis para dashboards
- [ ] Notificaciones en tiempo real con WebSockets
- [ ] Email automático de confirmación de reservas con PDF
- [ ] Gráficas interactivas con ApexCharts
- [ ] Sistema de puntos de lealtad
- [ ] Exportación a Excel además de PDF
- [ ] Dashboard mobile mejorado
- [ ] Integración con pasarelas de pago en tiempo real

## 11. TESTING RÁPIDO

```bash
# Verificar endpoints
curl http://localhost:8000/api/dashboard/stats
curl http://localhost:8000/api/dashboard/ingresos-mensuales
curl http://localhost:8000/api/dashboard/ocupacion-hoteles

# Generar PDF
curl http://localhost:8000/api/reservas/1/pdf > recibo.pdf

# Ver datos del usuario
curl http://localhost:8000/api/cliente/1/reservas
curl http://localhost:8000/api/cliente/1/paquetes
```

## 12. NOTAS IMPORTANTES

⚠️ **SEGURIDAD:**
- Los endpoints /api/me requieren autenticación (implementar JWT)
- Los PDFs deben generarse solo para usuarios autorizados
- Validar permisos en cada endpoint

⚠️ **PERFORMANCE:**
- Las vistas SQL con GROUP BY pueden ser lentas con millones de registros
- Considerar agregar índices compuestos después de medir
- Usar caché para datos estáticos (hoteles, paquetes)

⚠️ **COMPATIBILIDAD:**
- Verificar que las funciones de fecha en PostgreSQL sean compatibles
- En MySQL usar DATE_FORMAT en lugar de DATE_TRUNC
- SQLite tiene sintaxis diferente para agregaciones

✅ **PRÓXIMOS PASOS:**
1. Reemplazar dashboard.html por dashboard-premium.html en rutas
2. Reemplazar perfil.html por perfil-premium.html en rutas
3. Incluir enhanced_api.py en main.py
4. Ejecutar sql_optimization.sql en la BD
5. Probar endpoints con Postman o curl
6. Verificar que los PDFs se generen correctamente
