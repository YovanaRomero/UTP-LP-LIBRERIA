from pydantic import BaseModel
from typing import Optional


class ProductoBase(BaseModel):
    producto_nombre: str
    producto_descripcion: str
    producto_precio: float
    categoria_id: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    producto_nombre: Optional[str] = None
    producto_descripcion: Optional[str] = None
    producto_precio: Optional[float] = None
    categoria_id: Optional[int] = None


class Producto(ProductoBase):
    producto_id: int

    class Config:
        from_attributes = True
