from pydantic import BaseModel
from typing import Optional


class DetalleBase(BaseModel):
    detalle_producto_id: int
    detalle_secuencia: Optional[int] = None
    detalle_producto_precio: Optional[float] = None
    detalle_cantidad: Optional[int] = None


class DetalleCreate(DetalleBase):
    pass


class DetalleUpdate(BaseModel):
    detalle_secuencia: Optional[int] = None
    detalle_producto_precio: Optional[float] = None
    detalle_cantidad: Optional[int] = None


class Detalle(DetalleBase):
    detalle_pedido_id: int

    class Config:
        from_attributes = True
