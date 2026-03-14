from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class TenantRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    ruc: Optional[str] = None
    telefono: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    tenant_id: Optional[UUID] = None
    email: Optional[str] = None
    rol: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    nombre: str
    email: str
    rol: str
    tenant_id: UUID

    class Config:
        from_attributes = True