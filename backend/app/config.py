from dotenv import load_dotenv
import os
from typing import List

# Cargar variables de entorno desde un archivo .env si existe
load_dotenv()


class Settings:
    # Base de datos
    DB_HOST: str = os.getenv("DB_HOST", "173.249.41.159")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME", "salesdb")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "my801521my")

    # Aplicación
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    # Orígenes permitidos para CORS (coma-separados)
    # Ejemplo: "http://localhost:4200,http://frontend:80"
    CORS_ORIGINS: List[str] = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:4200,http://frontend:80").split(",") if o.strip()]


# Instancia global de settings
settings = Settings()
