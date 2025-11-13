from pydantic import BaseModel
from typing import Optional


class ProductoBase(BaseModel):
    producto_nombre: str
    producto_descripcion: str
    producto_precio: float
    producto_stock: int
    producto_color: Optional[str] = None
    producto_dimensiones: Optional[str] = None
    producto_estado: Optional[int] = None
    categoria_categoria_id: int


class ProductoCreate(ProductoBase):
    producto_serie: Optional[str] = None


class ProductoUpdate(BaseModel):
    producto_nombre: Optional[str] = None
    producto_descripcion: Optional[str] = None
    producto_precio: Optional[float] = None
    producto_stock: Optional[int] = None
    producto_color: Optional[str] = None
    producto_dimensiones: Optional[str] = None
    producto_estado: Optional[int] = None
    categoria_categoria_id: Optional[int] = None


class Producto(ProductoBase):
    producto_id: int
    producto_guid: Optional[str] = None
    producto_serie: Optional[str] = None

    class Config:
        from_attributes = True
