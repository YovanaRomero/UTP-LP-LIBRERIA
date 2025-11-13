from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import Categoria, CategoriaCreate, CategoriaUpdate
from ..services import CategoriaService

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=List[Categoria], status_code=status.HTTP_200_OK)
def listar_categorias():
    """Listar todas las categorías"""
    categorias = CategoriaService.get_all_categorias()
    return categorias


@router.get("/{categoria_id}", response_model=Categoria, status_code=status.HTTP_200_OK)
def obtener_categoria(categoria_id: int):
    """Obtener una categoría por ID"""
    categoria = CategoriaService.get_categoria_by_id(categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return categoria


@router.post("/", response_model=Categoria, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: CategoriaCreate):
    """Crear una nueva categoría"""
    nueva_categoria = CategoriaService.create_categoria(categoria)
    if nueva_categoria is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la categoría"
        )
    return nueva_categoria


@router.put("/{categoria_id}", response_model=Categoria, status_code=status.HTTP_200_OK)
def actualizar_categoria(categoria_id: int, categoria: CategoriaUpdate):
    """Actualizar una categoría existente"""
    categoria_actualizada = CategoriaService.update_categoria(categoria_id, categoria)
    if categoria_actualizada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return categoria_actualizada


@router.delete("/{categoria_id}", status_code=status.HTTP_200_OK)
def eliminar_categoria(categoria_id: int):
    """Eliminar una categoría"""
    eliminada = CategoriaService.delete_categoria(categoria_id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return {"message": f"Categoría con ID {categoria_id} eliminada correctamente"}
