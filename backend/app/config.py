from dotenv import load_dotenv
import os
import socket
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
    # Pool de conexiones
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))

    # Aplicación
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    # Orígenes permitidos para CORS (coma-separados)
    # Ejemplo: "http://localhost:4200,http://frontend:80"
    CORS_ORIGINS: List[str] = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:4200,http://frontend:80").split(",") if o.strip()]

    # Nombre del equipo o nombre del equipo de trabajo para mostrar en el título
    TEAM_NAME: str = os.getenv("TEAM_NAME", socket.gethostname())

    # Información de licencia
    LICENSE_NAME: str = os.getenv("LICENSE_NAME", "MIT")
    LICENSE_URL: str = os.getenv("LICENSE_URL", "https://opensource.org/licenses/MIT")


# Instancia global de settings
settings = Settings()
