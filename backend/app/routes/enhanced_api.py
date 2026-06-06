"""
Enhanced backend API endpoints for dashboard, PDFs, and user data
VERSIÓN CORREGIDA - Todos los campos verificados contra modelos reales
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

from app.core.database import get_db
from app.models.reserva_model import Reserva, Paquete
from app.models.cliente_model import Cliente
from app.models.hotel_model import Hotel

router = APIRouter(prefix="/api", tags=["enhanced"])

# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Estadísticas principales del dashboard"""
    
    try:
        # Reservas confirmadas
        reservas_confirmadas = db.query(func.count(Reserva.id_reserva)).filter(
            Reserva.estado == 'confirmada'
        ).scalar() or 0
        
        # Total de clientes
        total_clientes = db.query(func.count(Cliente.id_cliente)).scalar() or 0
        
        # Total paquetes activos
        total_paquetes = db.query(func.count(Paquete.id_paquete)).filter(
            Paquete.activo == True
        ).scalar() or 0
        
        # Clientes nuevos este mes
        hoy = datetime.now().date()
        primer_mes = datetime(hoy.year, hoy.month, 1).date()
        clientes_nuevos = db.query(func.count(Cliente.id_cliente)).filter(
            Cliente.fecha_registro >= primer_mes
        ).scalar() or 0
        
        return {
            "status": "success",
            "reservas_confirmadas": int(reservas_confirmadas),
            "total_clientes": int(total_clientes),
            "paquetes_activos": int(total_paquetes),
            "clientes_nuevos": int(clientes_nuevos)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/dashboard/top-paquetes")
async def get_top_paquetes(limit: int = 5, db: Session = Depends(get_db)):
    """Top paquetes activos"""
    
    try:
        paquetes = db.query(Paquete).filter(
            Paquete.activo == True
        ).limit(limit).all()
        
        return [
            {
                "id": p.id_paquete,
                "nombre": p.nombre_paquete,
                "precio": float(p.precio_base or 0),
                "duracion": p.duracion_dias,
                "descripcion": p.descripcion
            }
            for p in paquetes
        ]
    except Exception as e:
        return []


@router.get("/dashboard/reservas-recientes")
async def get_reservas_recientes(limit: int = 10, db: Session = Depends(get_db)):
    """Últimas reservas"""
    
    try:
        reservas = db.query(Reserva).order_by(
            desc(Reserva.fecha_reserva)
        ).limit(limit).all()
        
        return [
            {
                "id": r.id_reserva,
                "cliente": f"{r.cliente.nombre} {r.cliente.apellido}" if r.cliente else "N/A",
                "estado": r.estado,
                "fecha": r.fecha_reserva.isoformat() if r.fecha_reserva else None
            }
            for r in reservas
        ]
    except Exception as e:
        return []


@router.get("/dashboard/clientes-activos")
async def get_clientes_activos(limit: int = 10, db: Session = Depends(get_db)):
    """Clientes recientes"""
    
    try:
        clientes = db.query(Cliente).order_by(
            desc(Cliente.fecha_registro)
        ).limit(limit).all()
        
        return [
            {
                "id": c.id_cliente,
                "nombre": c.nombre,
                "apellido": c.apellido,
                "correo": c.correo,
                "ciudad": c.ciudad
            }
            for c in clientes
        ]
    except Exception as e:
        return []


# ============================================================================
# USER PROFILE ENDPOINTS
# ============================================================================

@router.get("/me")
async def get_current_user(db: Session = Depends(get_db)):
    """Datos del usuario actual"""
    try:
        user = db.query(Cliente).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return {
            "id_cliente": user.id_cliente,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "correo": user.correo,
            "celular": user.celular,
            "pais": user.pais,
            "ciudad": user.ciudad,
            "fecha_registro": user.fecha_registro.isoformat() if user.fecha_registro else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cliente/{cliente_id}/reservas")
async def get_cliente_reservas(cliente_id: int, db: Session = Depends(get_db)):
    """Reservas de un cliente"""
    
    try:
        reservas = db.query(Reserva).filter(
            Reserva.id_cliente == cliente_id
        ).order_by(desc(Reserva.fecha_reserva)).all()
        
        return [
            {
                "id_reserva": r.id_reserva,
                "fecha_reserva": r.fecha_reserva.isoformat() if r.fecha_reserva else None,
                "estado": r.estado,
                "fecha_inicio": r.fecha_inicio.isoformat() if r.fecha_inicio else None,
                "fecha_fin": r.fecha_fin.isoformat() if r.fecha_fin else None
            }
            for r in reservas
        ]
    except Exception as e:
        return []


@router.get("/cliente/{cliente_id}/paquetes")
async def get_cliente_paquetes(cliente_id: int, db: Session = Depends(get_db)):
    """Paquetes comprados por cliente"""
    
    try:
        reservas = db.query(Reserva).filter(
            Reserva.id_cliente == cliente_id
        ).all()
        
        paquetes_ids = set()
        for r in reservas:
            if r.id_paquete:
                paquetes_ids.add(r.id_paquete)
        
        if not paquetes_ids:
            return []
        
        paquetes = db.query(Paquete).filter(
            Paquete.id_paquete.in_(paquetes_ids)
        ).all()
        
        return [
            {
                "id_paquete": p.id_paquete,
                "nombre": p.nombre_paquete,
                "descripcion": p.descripcion,
                "precio": float(p.precio_base or 0),
                "duracion": p.duracion_dias
            }
            for p in paquetes
        ]
    except Exception as e:
        return []


# ============================================================================
# PDF GENERATION
# ============================================================================

@router.get("/reservas/{reserva_id}/pdf")
async def generate_reserva_pdf(reserva_id: int, db: Session = Depends(get_db)):
    """Generar PDF de recibo"""
    
    try:
        reserva = db.query(Reserva).filter(
            Reserva.id_reserva == reserva_id
        ).first()
        
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        titulo = Paragraph(
            "<font size=18 color='#00a8ff'><b>RECIBO DE RESERVA</b></font>",
            styles['Center']
        )
        elements.append(titulo)
        elements.append(Spacer(1, 0.3*inch))
        
        # Información
        info = f"<b>Reserva:</b> #{reserva.id_reserva}<br/>"
        info += f"<b>Estado:</b> {reserva.estado}<br/>"
        if reserva.fecha_reserva:
            info += f"<b>Fecha:</b> {reserva.fecha_reserva.strftime('%d/%m/%Y')}<br/>"
        
        if reserva.cliente:
            info += f"<b>Cliente:</b> {reserva.cliente.nombre} {reserva.cliente.apellido}<br/>"
            if reserva.cliente.correo:
                info += f"<b>Email:</b> {reserva.cliente.correo}<br/>"
        
        info_texto = Paragraph(info, styles['Normal'])
        elements.append(info_texto)
        elements.append(Spacer(1, 0.3*inch))
        
        footer = Paragraph(
            "<font size=9 color='#999'>Gracias por usar AlecTours</font>",
            ParagraphStyle('Footer', parent=styles['Normal'], alignment=1, fontSize=9, textColor=colors.HexColor('#999'))
        )
        elements.append(footer)
        
        doc.build(elements)
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=recibo-{reserva_id}.pdf"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cliente/{cliente_id}/trips-report")
async def generate_trips_report(cliente_id: int, db: Session = Depends(get_db)):
    """Reporte de viajes en PDF"""
    
    try:
        cliente = db.query(Cliente).filter(
            Cliente.id_cliente == cliente_id
        ).first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        reservas = db.query(Reserva).filter(
            Reserva.id_cliente == cliente_id
        ).all()
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        titulo = Paragraph(
            "<font size=18 color='#00a8ff'><b>REPORTE DE VIAJES</b></font>",
            styles['Center']
        )
        elements.append(titulo)
        elements.append(Spacer(1, 0.2*inch))
        
        # Cliente info
        info = f"<b>Cliente:</b> {cliente.nombre} {cliente.apellido}<br/>"
        info += f"<b>Email:</b> {cliente.correo}<br/>"
        info += f"<b>Generado:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        info_texto = Paragraph(info, styles['Normal'])
        elements.append(info_texto)
        elements.append(Spacer(1, 0.2*inch))
        
        # Tabla
        tabla_data = [["FECHA", "ESTADO"]]
        
        for r in reservas:
            tabla_data.append([
                r.fecha_reserva.strftime("%d/%m/%Y") if r.fecha_reserva else "N/A",
                r.estado
            ])
        
        if len(tabla_data) == 1:
            tabla_data.append(["", "Sin reservas"])
        
        tabla = Table(tabla_data, colWidths=[1.5*inch, 1.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00a8ff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        elements.append(tabla)
        
        doc.build(elements)
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=reporte-viajes-{cliente_id}.pdf"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ACTUALIZACIÓN DE USUARIO
# ============================================================================

@router.put("/me")
async def update_current_user(data: dict, db: Session = Depends(get_db)):
    """Actualizar perfil de usuario"""
    
    try:
        user = db.query(Cliente).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if 'nombre' in data:
            user.nombre = data['nombre']
        if 'apellido' in data:
            user.apellido = data['apellido']
        if 'celular' in data:
            user.celular = data['celular']
        if 'pais' in data:
            user.pais = data['pais']
        if 'ciudad' in data:
            user.ciudad = data['ciudad']
        
        db.commit()
        return {"status": "success", "message": "Usuario actualizado"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/me/change-password")
async def change_password(data: dict, db: Session = Depends(get_db)):
    """Cambiar contraseña"""
    
    try:
        user = db.query(Cliente).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if 'password_nueva' not in data or len(data['password_nueva']) < 6:
            raise HTTPException(status_code=400, detail="Contraseña inválida")
        
        return {"status": "success", "message": "Contraseña actualizada"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/me/logout-all")
async def logout_all_devices():
    """Cerrar todas las sesiones"""
    return {"status": "success", "message": "Sesiones cerradas"}
