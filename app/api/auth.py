from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.auth import TenantRegistro, UserLogin, Token, UserResponse
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", response_model=UserResponse)
def registro(data: TenantRegistro, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    existe = db.query(User).filter(User.email == data.email).first()
    if existe:
        raise HTTPException(
            status_code=400,
            detail="Este email ya está registrado"
        )
    
    # Crear el tenant (la gestora)
    tenant = Tenant(
        nombre=data.nombre,
        email=data.email,
        ruc=data.ruc,
        telefono=data.telefono
    )
    db.add(tenant)
    db.flush()

    # Crear el usuario admin de ese tenant
    user = User(
        tenant_id=tenant.id,
        nombre=data.nombre,
        email=data.email,
        password_hash=get_password_hash(data.password),
        rol="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    # Buscar usuario
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos"
        )
    
    if not user.activo:
        raise HTTPException(
            status_code=401,
            detail="Usuario inactivo"
        )

    # Crear token
    token = create_access_token(
        data={
            "user_id": str(user.id),
            "tenant_id": str(user.tenant_id),
            "email": user.email,
            "rol": user.rol
        },
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": token, "token_type": "bearer"}