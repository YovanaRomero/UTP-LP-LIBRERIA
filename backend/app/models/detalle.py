from pydantic import BaseModel, Field
from typing import Optional


# ==========================
# BASE DEL DETALLE
# ==========================
class DetalleBase(BaseModel):
    detalle_producto_id: int = Field(..., description="ID del producto")
    detalle_secuencia: Optional[int] = Field(
        None, description="Secuencia del detalle dentro del pedido"
    )
    detalle_producto_precio: Optional[float] = Field(
        None, ge=0, description="Precio unitario del producto"
    )
    detalle_cantidad: Optional[int] = Field(
        None, ge=1, description="Cantidad del producto"
    )


# ==========================
# CREACIÓN DEL DETALLE
# ==========================
class DetalleCreate(DetalleBase):
    pass


# ==========================
# ACTUALIZACIÓN DEL DETALLE
# ==========================
class DetalleUpdate(BaseModel):
    detalle_secuencia: Optional[int] = Field(None, ge=1)
    detalle_producto_precio: Optional[float] = Field(None, ge=0)
    detalle_cantidad: Optional[int] = Field(None, ge=1)


# ==========================
# RESPUESTA / LECTURA
# ==========================
class Detalle(DetalleBase):
    detalle_pedido_id: int = Field(..., description="ID del pedido asociado")

    class Config:
        from_attributes = True