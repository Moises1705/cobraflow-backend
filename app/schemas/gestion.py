from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class GestionCreate(BaseModel):
    deudor_id: UUID
    tipo: str  # call, campo, whatsapp, email
    resultado: Optional[str] = None
    comentario: Optional[str] = None
    monto_prometido: Optional[str] = None
    fecha_promesa: Optional[datetime] = None

class GestionResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    deudor_id: UUID
    user_id: UUID
    tipo: str
    resultado: Optional[str] = None
    comentario: Optional[str] = None
    monto_prometido: Optional[str] = None
    fecha_promesa: Optional[datetime] = None
    fecha_gestion: datetime
    created_at: datetime

    class Config:
        from_attributes = True