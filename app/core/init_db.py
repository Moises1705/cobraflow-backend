from app.core.database import engine, Base
from app.models.tenant import Tenant
from app.models.user import User
from app.models.deudor import Deudor
from app.models.gestion import Gestion

def init_db():
    print("🦜 Creando tablas de CobraFlow...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")

if __name__ == "__main__":
    init_db()