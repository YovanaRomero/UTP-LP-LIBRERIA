from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import (
    categorias_router,
    productos_router,
    clientes_router,
    usuarios_router,
    pedidos_router,
)
from .config import settings

app = FastAPI(
    title=f"API Libreria Virtual - {settings.TEAM_NAME}",
    version="1.0.0",
    description="API REST para gestión de librería virtual (categorías, productos, clientes, usuarios, pedidos)",   
    license_info={
        "name": settings.LICENSE_NAME,
        "url": settings.LICENSE_URL,
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Configuración CORS para permitir el frontend de Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://frontend:80"],  # URLs del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(categorias_router)
app.include_router(productos_router)
app.include_router(clientes_router)
app.include_router(usuarios_router)
app.include_router(pedidos_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)