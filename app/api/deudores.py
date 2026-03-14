from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import pandas as pd
import io
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.deudor import Deudor
from app.schemas.deudor import DeudorCreate, DeudorUpdate, DeudorResponse

router = APIRouter(prefix="/deudores", tags=["Deudores"])

@router.get("/", response_model=List[DeudorResponse])
def listar_deudores(
    skip: int = 0,
    limit: int = 100,
    etapa: str = None,
    estado: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Deudor).filter(Deudor.tenant_id == current_user.tenant_id)
    if etapa:
        query = query.filter(Deudor.etapa == etapa)
    if estado:
        query = query.filter(Deudor.estado == estado)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=DeudorResponse)
def crear_deudor(
    data: DeudorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deudor = Deudor(**data.model_dump(), tenant_id=current_user.tenant_id)
    db.add(deudor)
    db.commit()
    db.refresh(deudor)
    return deudor

@router.get("/{deudor_id}", response_model=DeudorResponse)
def obtener_deudor(
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
    return deudor

@router.put("/{deudor_id}", response_model=DeudorResponse)
def actualizar_deudor(
    deudor_id: UUID,
    data: DeudorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deudor = db.query(Deudor).filter(
        Deudor.id == deudor_id,
        Deudor.tenant_id == current_user.tenant_id
    ).first()
    if not deudor:
        raise HTTPException(status_code=404, detail="Deudor no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(deudor, key, value)
    db.commit()
    db.refresh(deudor)
    return deudor

@router.post("/importar-excel")
def importar_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos Excel")
    
    contents = file.file.read()
    df = pd.read_excel(io.BytesIO(contents))
    
    columnas_requeridas = ["codigo_usuario", "nombre", "monto_deuda"]
    for col in columnas_requeridas:
        if col not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Columna requerida faltante: {col}"
            )
    
    creados = 0
    errores = 0
    for _, row in df.iterrows():
        try:
            deudor = Deudor(
                tenant_id=current_user.tenant_id,
                codigo_usuario=str(row["codigo_usuario"]),
                codigo_judicial=str(row.get("codigo_judicial", "")) or None,
                nombre=str(row["nombre"]),
                dni=str(row.get("dni", "")) or None,
                telefono=str(row.get("telefono", "")) or None,
                telefono_2=str(row.get("telefono_2", "")) or None,
                direccion=str(row.get("direccion", "")) or None,
                monto_deuda=float(row["monto_deuda"]),
                etapa=str(row.get("etapa", "prejudicial")),
            )
            db.add(deudor)
            creados += 1
        except Exception:
            errores += 1
    
    db.commit()
    return {
        "mensaje": f"Importación completada",
        "creados": creados,
        "errores": errores
    }