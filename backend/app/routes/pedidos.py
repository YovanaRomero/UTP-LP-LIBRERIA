from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from ..models import Pedido, PedidoCreate, PedidoUpdate
from ..services import PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


# ==========================
# LISTAR TODOS LOS PEDIDOS
# ==========================
@router.get("/", response_model=List[Pedido])
def listar_pedidos():
    return PedidoService.listar_pedidos()


# ==========================
# OBTENER PEDIDO POR ID
# ==========================
@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(pedido_id: int):
    pedido = PedidoService.obtener_pedido(pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


# ==========================
# CREAR PEDIDO COMPLETO
# ==========================
@router.post("/create", response_model=Pedido, status_code=201)
def crear_pedido(pedido: PedidoCreate):
    creado = PedidoService.create(pedido)
    if creado is None:
        raise HTTPException(status_code=400, detail="Error al crear pedido")
    return creado


# ==========================
# ACTUALIZAR PEDIDO
# ==========================
@router.put("/{pedido_id}", response_model=Pedido)
def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate):
    actualizado = PedidoService.actualizar_pedido(pedido_id, pedido)
    if actualizado is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado o no actualizado")
    return actualizado


# ==========================
# ELIMINAR PEDIDO
# ==========================
@router.delete("/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    ok = PedidoService.eliminar_pedido(pedido_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"message": "Pedido eliminado correctamente"}


# ==========================
# BUSCAR POR DNI DEL CLIENTE
# ==========================
@router.get("/buscar/cliente/{dni}", response_model=List[Pedido])
def buscar_por_dni_cliente(dni: str):
    resultados = PedidoService.buscar_por_dni_cliente(dni)
    return resultados


# ==========================
# BUSCAR POR DNI DEL DELIVERY
# ==========================
@router.get("/buscar/delivery/{dni}", response_model=List[Pedido])
def buscar_por_dni_delivery(dni: str):
    resultados = PedidoService.buscar_por_dni_delivery(dni)
    return resultados


# ==========================
# BUSCAR POR RANGO DE FECHAS
# ==========================
@router.get("/buscar/fechas", response_model=List[Pedido])
def buscar_por_rango_fechas(
    desde: str = Query(..., description="Fecha inicial YYYY-MM-DD"),
    hasta: str = Query(..., description="Fecha final YYYY-MM-DD")
):
    resultados = PedidoService.buscar_por_rango_fechas(desde, hasta)
    return resultados


# ==========================
# REGISTRAR ENTREGA DEL PEDIDO
# ==========================
@router.post("/{pedido_id}/entrega")
def registrar_entrega(
    pedido_id: int,
    fecha_entrega: str = Query(..., description="Fecha de entrega YYYY-MM-DD"),
    observaciones: Optional[str] = None
):
    actualizado = PedidoService.registrar_entrega(pedido_id, fecha_entrega, observaciones)

    if actualizado is None:
        raise HTTPException(404, "Pedido no encontrado o no se pudo registrar la entrega")

    return {"message": "Entrega registrada correctamente", "pedido": actualizado}