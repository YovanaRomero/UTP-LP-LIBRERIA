from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .models import Categoria, CategoriaCreate, CategoriaUpdate
from .categoria_service import CategoriaService

app = FastAPI(title="API SalesDB", version="1.0.0")

# Configuración CORS para permitir el frontend de Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://frontend:80"],  # URLs del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/categorias", response_model=List[Categoria], status_code=status.HTTP_200_OK)
def listar_categorias():
    """Listar todas las categorías"""
    categorias = CategoriaService.get_all_categorias()
    return categorias

@app.get("/categorias/{categoria_id}", response_model=Categoria, status_code=status.HTTP_200_OK)
def obtener_categoria(categoria_id: int):
    """Obtener una categoría por ID"""
    categoria = CategoriaService.get_categoria_by_id(categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return categoria

@app.post("/categorias", response_model=Categoria, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: CategoriaCreate):
    """Crear una nueva categoría"""
    nueva_categoria = CategoriaService.create_categoria(categoria)
    if nueva_categoria is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la categoría"
        )
    return nueva_categoria

@app.put("/categorias/{categoria_id}", response_model=Categoria, status_code=status.HTTP_200_OK)
def actualizar_categoria(categoria_id: int, categoria: CategoriaUpdate):
    """Actualizar una categoría existente"""
    categoria_actualizada = CategoriaService.update_categoria(categoria_id, categoria)
    if categoria_actualizada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return categoria_actualizada


@app.delete("/categorias/{categoria_id}", status_code=status.HTTP_200_OK)
def eliminar_categoria(categoria_id: int):
    """Eliminar una categoría"""
    eliminada = CategoriaService.delete_categoria(categoria_id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return {"message": f"Categoría con ID {categoria_id} eliminada correctamente"}

# Health check para verificar la conexión a la base de datos
@app.get("/health")
def health_check():
    """Verificar el estado de la API y la conexión a la base de datos"""
    connection = CategoriaService.get_all_categorias()
    db_status = "connected" if connection is not None else "disconnected"

    return {
        "status": "healthy",
        "database": db_status,
        "message": "API de categorías funcionando correctamente"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)