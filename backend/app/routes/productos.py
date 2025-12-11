from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import Producto, ProductoCreate, ProductoUpdate
from ..services import ProductoService

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[Producto], status_code=status.HTTP_200_OK)
def listar_productos():
    """Listar todos los productos"""
    productos = ProductoService.get_all_productos()
    return productos


@router.get("/{producto_id}", response_model=Producto, status_code=status.HTTP_200_OK)
def obtener_producto(producto_id: int):
    """Obtener un producto por ID"""
    producto = ProductoService.get_producto_by_id(producto_id)
    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return producto


@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    nuevo_producto = ProductoService.create_producto(producto)
    if nuevo_producto is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el producto"
        )
    return nuevo_producto


@router.put("/{producto_id}", response_model=Producto, status_code=status.HTTP_200_OK)
def actualizar_producto(producto_id: int, producto: ProductoUpdate):
    """Actualizar un producto existente"""
    producto_actualizado = ProductoService.update_producto(producto_id, producto)
    if producto_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return producto_actualizado


@router.delete("/{producto_id}", status_code=status.HTTP_200_OK)
def eliminar_producto(producto_id: int):
    """Eliminar un producto"""
    eliminado = ProductoService.delete_producto(producto_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return {"message": f"Producto con ID {producto_id} eliminado correctamente"}


#Grafico con panda de stock por producto
from fastapi.responses import StreamingResponse

@router.get("/stock/data")
def stock_productos_data():
    """Retorna stock en formato JSON."""
    return ProductoService.obtener_stock_productos()

#Grafico en el cual se genera
@router.get("/stock/grafico")
def stock_productos_grafico():
    img = ProductoService.generar_grafico_stock()
    return StreamingResponse(img, media_type="image/png")