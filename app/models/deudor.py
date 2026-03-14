from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Deudor(Base):
    __tablename__ = "deudores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Datos del deudor
    codigo_usuario = Column(String(50), nullable=False)
    codigo_judicial = Column(String(50), nullable=True)
    nombre = Column(String(150), nullable=False)
    dni = Column(String(20), nullable=True)
    telefono = Column(String(20), nullable=True)
    telefono_2 = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    email = Column(String(100), nullable=True)
    
    # Datos de la deuda
    monto_deuda = Column(Float, nullable=False, default=0)
    moneda = Column(String(10), default="PEN")
    etapa = Column(String(30), default="prejudicial")  # prejudicial, judicial, castigo
    estado = Column(String(30), default="activo")  # activo, pagado, incobrable
    
    # Fechas
    fecha_asignacion = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tenant = relationship("Tenant", backref="deudores")
    gestiones = relationship("Gestion", backref="deudor")