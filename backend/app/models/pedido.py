from pydantic import BaseModel, Field
from typing import Optional, List
from .detalle import Detalle, DetalleCreate


# ==========================
# BASE DEL PEDIDO
# ==========================
class PedidoBase(BaseModel):
    pedido_numero: Optional[str] = Field(None, description="Número del pedido")
    pedido_fecha_registro: Optional[str] = Field(None, description="Fecha de registro")
    pedido_fecha_entrega: Optional[str] = Field(None, description="Fecha de entrega")
    pedido_personal_delivery: Optional[str] = Field(None, description="Personal encargado del delivery")
    pedido_observaciones: Optional[str] = Field(None, description="Observaciones del pedido")
    cliente_cliente_id: int = Field(..., description="ID del cliente asociado")
    pedido_subtotal: Optional[float] = Field(None, ge=0, description="Subtotal del pedido")
    pedido_igv: Optional[float] = Field(None, ge=0, description="IGV del pedido")
    pedido_total: Optional[float] = Field(None, ge=0, description="Total del pedido")
    pedido_estado: Optional[int] = Field(1, description="Estado del pedido (1=Registrado, 2=Entregado, 0=Anulado)")


# ==========================
# MODELO PARA CREAR PEDIDO
# ==========================
class PedidoCreate(PedidoBase):
    detalles: Optional[List[DetalleCreate]] = Field(
        [], description="Lista de detalles del pedido"
    )


# ==========================
# MODELO PARA ACTUALIZAR PEDIDO
# ==========================
class PedidoUpdate(BaseModel):
    pedido_numero: Optional[str] = None
    pedido_fecha_registro: Optional[str] = None
    pedido_fecha_entrega: Optional[str] = None
    pedido_personal_delivery: Optional[str] = None
    pedido_observaciones: Optional[str] = None
    cliente_cliente_id: Optional[int] = None
    pedido_subtotal: Optional[float] = None
    pedido_igv: Optional[float] = None
    pedido_total: Optional[float] = None
    pedido_estado: Optional[int] = None
    detalles: Optional[List[DetalleCreate]] = None


# ==========================
# MODELO DE RESPUESTA / LECTURA
# ==========================
class Pedido(PedidoBase):
    pedido_id: int
    pedido_guid: Optional[str] = None
    detalles: Optional[List[Detalle]] = []

    class Config:
        from_attributes = True