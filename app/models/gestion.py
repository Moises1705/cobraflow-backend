from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Gestion(Base):
    __tablename__ = "gestiones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    deudor_id = Column(UUID(as_uuid=True), ForeignKey("deudores.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Tipo de gestión
    tipo = Column(String(20), nullable=False)  # call, campo, whatsapp, email
    resultado = Column(String(50), nullable=True)  # contactado, no_contesta, promesa_pago, etc
    comentario = Column(Text, nullable=True)

    # Promesa de pago
    monto_prometido = Column(String(20), nullable=True)
    fecha_promesa = Column(DateTime(timezone=True), nullable=True)

    # Fechas
    fecha_gestion = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tenant = relationship("Tenant", backref="gestiones")
    gestor = relationship("User", backref="gestiones")