from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

# Import models and services when implemented
# from ..models import Producto, ProductoCreate, ProductoUpdate
# from ..producto_service import ProductoService

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", status_code=status.HTTP_200_OK)
def listar_productos():
    """Listado de productos (placeholder)."""
    # Replace with: return ProductoService.get_all_productos()
    return []


@router.get("/{producto_id}", status_code=status.HTTP_200_OK)
def obtener_producto(producto_id: int):
    """Obtener producto por ID (placeholder)."""
    # Replace with actual service lookup
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No implementado")
