from pydantic import BaseModel
from typing import Optional, List
from .detalle import Detalle, DetalleCreate


class PedidoBase(BaseModel):
    pedido_numero: Optional[str] = None
    pedido_fecha_registro: Optional[str] = None
    pedido_fecha_entrega: Optional[str] = None
    pedido_personal_delivery: Optional[str] = None
    pedido_observaciones: Optional[str] = None
    cliente_cliente_id: int
    pedido_subtotal: Optional[float] = None
    pedido_igv: Optional[float] = None
    pedido_total: Optional[float] = None
    pedido_estado: Optional[int] = None


class PedidoCreate(PedidoBase):
    detalles: Optional[List[DetalleCreate]] = None


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


class Pedido(PedidoBase):
    pedido_id: int
    pedido_guid: Optional[str] = None
    detalles: Optional[List[Detalle]] = None

    class Config:
        from_attributes = True
