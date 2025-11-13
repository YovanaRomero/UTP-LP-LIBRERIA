from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .services import CategoriaService
from .routes import categorias_router, productos_router

app = FastAPI(title="API Libreria Virtual", version="1.0.0")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)