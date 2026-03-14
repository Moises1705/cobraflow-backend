from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CobraFlow"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    DATABASE_URL: str = ""
    SECRET_KEY: str = "cobraflow-secret-key-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()