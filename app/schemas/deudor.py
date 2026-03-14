from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DeudorCreate(BaseModel):
    codigo_usuario: str
    codigo_judicial: Optional[str] = None
    nombre: str
    dni: Optional[str] = None
    telefono: Optional[str] = None
    telefono_2: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    monto_deuda: float
    moneda: Optional[str] = "PEN"
    etapa: Optional[str] = "prejudicial"

class DeudorUpdate(BaseModel):
    telefono: Optional[str] = None
    telefono_2: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    monto_deuda: Optional[float] = None
    etapa: Optional[str] = None
    estado: Optional[str] = None

class DeudorResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    codigo_usuario: str
    codigo_judicial: Optional[str] = None
    nombre: str
    dni: Optional[str] = None
    telefono: Optional[str] = None
    telefono_2: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    monto_deuda: float
    moneda: str
    etapa: str
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True