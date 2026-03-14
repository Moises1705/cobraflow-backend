from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.deudores import router as deudores_router
from app.api.gestiones import router as gestiones_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="CRM Financiero para gestoras de cobranza"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(deudores_router)
app.include_router(gestiones_router)

@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "🦜 CobraFlow corriendo"
    }

@app.get("/health")
def health():
    return {"status": "ok"}