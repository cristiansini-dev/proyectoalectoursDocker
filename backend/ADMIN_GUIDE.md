# Sistema Administrativo Visual - AlecTours

## 📋 Descripción

Sistema administrativo completo desarrollado con **FastAPI** y **Jinja2 Templates** para gestionar:
- 🏨 Hoteles y Habitaciones
- 👥 Clientes y Empleados
- 👤 Usuarios del Sistema
- 📅 Reservas
- 🎁 Paquetes Turísticos
- 💳 Pagos

## 🚀 Características

✅ Dashboard principal con estadísticas
✅ CRUD completo para cada módulo
✅ Listados con búsqueda y paginación
✅ Formularios dinámicos con validación
✅ Interfaz responsiva con Bootstrap 5
✅ Notificaciones y mensajes de confirmación
✅ Consumo de APIs existentes (sin duplicar lógica)
✅ Diseño moderno y profesional
✅ Menú lateral dinámico
✅ Sistema de alertas personalizado

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── templates/          # Plantillas HTML
│   │   ├── layouts/        # Layouts base (base.html, sidebar, navbar, etc)
│   │   ├── admin/          # Vistas administrativas
│   │   │   ├── dashboard.html
│   │   │   ├── hoteles/
│   │   │   ├── clientes/
│   │   │   ├── empleados/
│   │   │   ├── usuarios/
│   │   │   ├── reservas/
│   │   │   ├── paquetes/
│   │   │   └── pagos/
│   │   └── components/     # Componentes reutilizables
│   ├── static/             # Archivos estáticos
│   │   ├── css/
│   │   │   └── style.css   # Estilos personalizados
│   │   └── js/
│   │       ├── notifications.js    # Sistema de notificaciones
│   │       ├── crud-handler.js     # Manejador universal de CRUD
│   │       └── form-validator.js   # Validación de formularios
│   ├── routes/
│   │   ├── frontend_route.py       # Rutas del admin
│   │   └── ... (rutas de API)
│   └── main.py                     # Configuración de Jinja2
└── requirements.txt
```

## 🔧 Instalación

### 1. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

Las dependencias necesarias ya se han agregado a `requirements.txt`:
- `jinja2==3.1.2`
- `python-multipart==0.0.6`

### 2. Ejecutar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Acceder al admin

```
http://localhost:8000/admin
```

## 📖 Uso

### Dashboard Principal
- URL: `/admin`
- Estadísticas generales
- Accesos rápidos a módulos
- Estado del sistema

### Gestión de Hoteles
- **Listado**: `/admin/hoteles`
- **Crear**: `/admin/hoteles/nuevo`
- **Editar**: `/admin/hoteles/{id}/editar`
- Funciones: Crear, Leer, Actualizar, Eliminar, Buscar, Paginar

### Gestión de Clientes
- **Listado**: `/admin/clientes`
- **Crear**: `/admin/clientes/nuevo`
- **Editar**: `/admin/clientes/{id}/editar`
- Campos: Nombre, Apellido, Cédula, Email, Teléfono, Dirección, Ciudad, País

### Gestión de Empleados
- **Listado**: `/admin/empleados`
- **Crear**: `/admin/empleados/nuevo`
- **Editar**: `/admin/empleados/{id}/editar`
- Similar a clientes con campos adicionales

### Gestión de Usuarios
- **Listado**: `/admin/usuarios`
- Vista de cuentas de usuarios del sistema
- Info de estado y último acceso

### Gestión de Reservas
- **Listado**: `/admin/reservas`
- **Crear**: `/admin/reservas/nueva`
- **Editar**: `/admin/reservas/{id}/editar`
- Campos: Cliente, Habitación, Fechas, Costo Total

### Gestión de Paquetes
- **Listado**: `/admin/paquetes`
- **Crear**: `/admin/paquetes/nuevo`
- **Editar**: `/admin/paquetes/{id}/editar`
- Campos: Nombre, Descripción, Precio, Duración

### Gestión de Pagos
- **Listado**: `/admin/pagos`
- **Crear**: `/admin/pagos/nuevo`
- **Editar**: `/admin/pagos/{id}/editar`
- Campos: Reserva, Monto, Método de Pago, Estado

## 🎨 Componentes JavaScript

### notifications.js
Sistema de notificaciones y alertas:
```javascript
showSuccess('Mensaje de éxito');
showError('Mensaje de error');
showWarning('Advertencia');
showInfo('Información');
showSpinner('Cargando...');
showConfirm('¿Confirmar?', onConfirmCallback);
```

### crud-handler.js
Funciones universales para CRUD:
```javascript
fetchAPI('GET', '/api/endpoint');           // GET genérico
fetchList(endpoint, page, limit);           // Listar con paginación
fetchById(endpoint, id);                    // Obtener por ID
createRecord(endpoint, data);               // Crear
updateRecord(endpoint, id, data);           // Actualizar
deleteRecord(endpoint, id, onConfirm);      // Eliminar
loadTable(endpoint, tableId, columns);      // Cargar tabla
populateSelect(endpoint, selectId, ...);    // Llenar selects dinámicamente
```

### form-validator.js
Validación de formularios:
```javascript
validateForm(formId, rules);                // Validar formulario
validateEmail(email);                       // Validar email
validateCedula(cedula);                     // Validar cédula
validatePhone(phone);                       // Validar teléfono
setupFieldValidation(fieldId, rules);       // Validación en tiempo real
```

## 🎯 Características Avanzadas

### Búsqueda Local
Búsqueda en tiempo real en tablas (sin recargar desde API).

### Paginación Automática
Manejo automático de paginación en listados.

### Selects Dinámicos
Carga automática de datos en selects desde API.

### Validación Bidireccional
- Validación frontend (antes de enviar)
- Validación backend (Pydantic)

### Relaciones de Datos
Manejo correcto de Foreign Keys y relaciones SQLAlchemy.

### Manejo de Errores
Mensajes claros y específicos para cada tipo de error.

## 📝 Notas Técnicas

### Sin Duplicación de Lógica
- ✅ Reutiliza endpoints API existentes
- ✅ Reutiliza schemas Pydantic
- ✅ Reutiliza validaciones del backend

### Responsivo
- ✅ Funciona en desktop, tablet y móvil
- ✅ Bootstrap 5 para grid responsive
- ✅ Menú colapsable en móvil

### Reutilizable
- ✅ Componentes HTML modulares
- ✅ JavaScript genérico y flexible
- ✅ CSS compartido

## 🔐 Seguridad

- Los endpoints existentes mantienen su autenticación JWT
- Las rutas admin pueden protegerse agregando middleware de autenticación
- Validación en frontend y backend
- Protección contra XSS con Jinja2

## 🛠️ Customización

### Agregar Nuevo Módulo

1. Crear carpeta: `app/templates/admin/modulo/`
2. Crear `list.html` y `form.html`
3. Agregar rutas en `app/routes/frontend_route.py`
4. Agregar entrada en sidebar.html

### Cambiar Estilos

Editar `app/static/css/style.css` para personalizar colores y diseño.

### Agregar Funcionalidades

Los archivos JavaScript son modulares y fáciles de extender:
- `notifications.js` - Agregar nuevos tipos de notificaciones
- `crud-handler.js` - Agregar nuevas funciones de API
- `form-validator.js` - Agregar nuevos validadores

## 📦 API Endpoints Consumidos

El admin consume estos endpoints API existentes:

```
GET    /api/hoteles
POST   /api/hoteles
PUT    /api/hoteles/{id}
DELETE /api/hoteles/{id}

GET    /api/clientes
POST   /api/clientes
PUT    /api/clientes/{id}
DELETE /api/clientes/{id}

GET    /api/empleados
POST   /api/empleados
PUT    /api/empleados/{id}
DELETE /api/empleados/{id}

GET    /api/usuarios

GET    /api/reservas
POST   /api/reservas
PUT    /api/reservas/{id}
DELETE /api/reservas/{id}

GET    /api/paquetes
POST   /api/paquetes
PUT    /api/paquetes/{id}
DELETE /api/paquetes/{id}

GET    /api/pagos
POST   /api/pagos
PUT    /api/pagos/{id}
DELETE /api/pagos/{id}
```

## ✨ Ventajas del Sistema

✅ **Sin Backend Adicional**: Todo funciona dentro del FastAPI existente
✅ **Sin BD Modificada**: No toca Docker ni PostgreSQL
✅ **Código Limpio**: Modular y fácil de mantener
✅ **Escalable**: Fácil agregar nuevos módulos
✅ **Profesional**: Interfaz moderna y responsiva
✅ **Rápido**: Carga datos sin refresco de página (SPA)
✅ **Intuitivo**: Fácil de usar para administradores

## 🚀 Próximas Mejoras

- Agregar autenticación JWT en rutas admin
- Implementar logs de auditoría
- Agregar exportación a Excel/PDF
- Implementar gráficos de estadísticas
- Agregar búsqueda avanzada con filtros
- Implementar mensajes en tiempo real (WebSockets)
- Agregar importación de datos

## 📞 Soporte

Para dudas o problemas, revisar:
- Logs de FastAPI (UVICORN)
- Consola de navegador (Dev Tools)
- Respuestas de API en Network tab

---

**Versión**: 1.0.0
**Última Actualización**: 2026-06-05
