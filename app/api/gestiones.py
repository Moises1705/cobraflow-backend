from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.deudor import Deudor
from app.models.gestion import Gestion
from app.schemas.gestion import GestionCreate, GestionResponse

router = APIRouter(prefix="/gestiones", tags=["Gestiones"])

@router.post("/", response_model=GestionResponse)
def crear_gestion(
    data: GestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deudor = db.query(Deudor).filter(
        Deudor.id == data.deudor_id,
        Deudor.tenant_id == current_user.tenant_id
    ).first()
    if not deudor:
        raise HTTPException(status_code=404, detail="Deudor no encontrado")

    gestion = Gestion(
        tenant_id=current_user.tenant_id,
        deudor_id=data.deudor_id,
        user_id=current_user.id,
        tipo=data.tipo,
        resultado=data.resultado,
        comentario=data.comentario,
        monto_prometido=data.monto_prometido,
        fecha_promesa=data.fecha_promesa
    )
    db.add(gestion)
    db.commit()
    db.refresh(gestion)
    return gestion

@router.get("/deudor/{deudor_id}", response_model=List[GestionResponse])
def historial_deudor(
    deudor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deudor = db.query(Deudor).filter(
        Deudor.id == deudor_id,
        Deudor.tenant_id == current_user.tenant_id
    ).first()
    if not deudor:
        raise HTTPException(status_code=404, detail="Deudor no encontrado")

    return db.query(Gestion).f