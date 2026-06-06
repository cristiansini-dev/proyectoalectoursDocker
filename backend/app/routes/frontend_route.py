from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(tags=["Frontend Admin"])

# Setup templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ===================== DASHBOARD =====================

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Dashboard principal del admin"""
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


# ===================== HOTELES =====================

@router.get("/admin/hoteles", response_class=HTMLResponse)
async def admin_hoteles_list(request: Request):
    """Listado de hoteles"""
    return templates.TemplateResponse("admin/hoteles/list.html", {"request": request})


@router.get("/admin/hoteles/nuevo", response_class=HTMLResponse)
async def admin_hoteles_create(request: Request):
    """Formulario crear hotel"""
    return templates.TemplateResponse("admin/hoteles/form.html", {"request": request, "mode": "create"})


@router.get("/admin/hoteles/{hotel_id}/editar", response_class=HTMLResponse)
async def admin_hoteles_edit(request: Request, hotel_id: int):
    """Formulario editar hotel"""
    return templates.TemplateResponse("admin/hoteles/form.html", {"request": request, "mode": "edit", "hotel_id": hotel_id})


# ===================== CLIENTES =====================

@router.get("/admin/clientes", response_class=HTMLResponse)
async def admin_clientes_list(request: Request):
    """Listado de clientes"""
    return templates.TemplateResponse("admin/clientes/list.html", {"request": request})


@router.get("/admin/clientes/nuevo", response_class=HTMLResponse)
async def admin_clientes_create(request: Request):
    """Formulario crear cliente"""
    return templates.TemplateResponse("admin/clientes/form.html", {"request": request, "mode": "create"})


@router.get("/admin/clientes/{cliente_id}/editar", response_class=HTMLResponse)
async def admin_clientes_edit(request: Request, cliente_id: int):
    """Formulario editar cliente"""
    return templates.TemplateResponse("admin/clientes/form.html", {"request": request, "mode": "edit", "cliente_id": cliente_id})


# ===================== EMPLEADOS =====================

@router.get("/admin/empleados", response_class=HTMLResponse)
async def admin_empleados_list(request: Request):
    """Listado de empleados"""
    return templates.TemplateResponse("admin/empleados/list.html", {"request": request})


@router.get("/admin/empleados/nuevo", response_class=HTMLResponse)
async def admin_empleados_create(request: Request):
    """Formulario crear empleado"""
    return templates.TemplateResponse("admin/empleados/form.html", {"request": request, "mode": "create"})


@router.get("/admin/empleados/{empleado_id}/editar", response_class=HTMLResponse)
async def admin_empleados_edit(request: Request, empleado_id: int):
    """Formulario editar empleado"""
    return templates.TemplateResponse("admin/empleados/form.html", {"request": request, "mode": "edit", "empleado_id": empleado_id})


# ===================== USUARIOS =====================

@router.get("/admin/usuarios", response_class=HTMLResponse)
async def admin_usuarios_list(request: Request):
    """Listado de usuarios"""
    return templates.TemplateResponse("admin/usuarios/list.html", {"request": request})


# ===================== PERFIL Y CONFIGURACIÓN =====================

@router.get("/admin/perfil", response_class=HTMLResponse)
async def admin_perfil(request: Request):
    """Mi perfil y configuración"""
    return templates.TemplateResponse("admin/perfil.html", {"request": request})


# ===================== RESERVAS =====================

@router.get("/admin/reservas", response_class=HTMLResponse)
async def admin_reservas_list(request: Request):
    """Listado de reservas"""
    return templates.TemplateResponse("admin/reservas/list.html", {"request": request})


@router.get("/admin/reservas/nueva", response_class=HTMLResponse)
async def admin_reservas_create(request: Request):
    """Formulario crear reserva"""
    return templates.TemplateResponse("admin/reservas/form.html", {"request": request, "mode": "create"})


@router.get("/admin/reservas/{reserva_id}/editar", response_class=HTMLResponse)
async def admin_reservas_edit(request: Request, reserva_id: int):
    """Formulario editar reserva"""
    return templates.TemplateResponse("admin/reservas/form.html", {"request": request, "mode": "edit", "reserva_id": reserva_id})


# ===================== PAQUETES =====================

@router.get("/admin/paquetes", response_class=HTMLResponse)
async def admin_paquetes_list(request: Request):
    """Listado de paquetes"""
    return templates.TemplateResponse("admin/paquetes/list.html", {"request": request})


@router.get("/admin/paquetes/nuevo", response_class=HTMLResponse)
async def admin_paquetes_create(request: Request):
    """Formulario crear paquete"""
    return templates.TemplateResponse("admin/paquetes/form.html", {"request": request, "mode": "create"})


@router.get("/admin/paquetes/{paquete_id}/editar", response_class=HTMLResponse)
async def admin_paquetes_edit(request: Request, paquete_id: int):
    """Formulario editar paquete"""
    return templates.TemplateResponse("admin/paquetes/form.html", {"request": request, "mode": "edit", "paquete_id": paquete_id})


# ===================== PAGOS =====================

@router.get("/admin/pagos", response_class=HTMLResponse)
async def admin_pagos_list(request: Request):
    """Listado de pagos"""
    return templates.TemplateResponse("admin/pagos/list.html", {"request": request})


@router.get("/admin/pagos/nuevo", response_class=HTMLResponse)
async def admin_pagos_create(request: Request):
    """Formulario crear pago"""
    return templates.TemplateResponse("admin/pagos/form.html", {"request": request, "mode": "create"})


@router.get("/admin/pagos/{pago_id}/editar", response_class=HTMLResponse)
async def admin_pagos_edit(request: Request, pago_id: int):
    """Formulario editar pago"""
    return templates.TemplateResponse("admin/pagos/form.html", {"request": request, "mode": "edit", "pago_id": pago_id})
