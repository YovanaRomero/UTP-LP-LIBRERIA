from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import Pedido, PedidoCreate, PedidoUpdate
from ..services import PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.get("/", response_model=List[Pedido])
def listar_pedidos():
    return PedidoService.listar_pedidos()


@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(pedido_id: int):
    pedido = PedidoService.obtener_pedido(pedido_id)
    if pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    return pedido


@router.post("/", response_model=Pedido, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: PedidoCreate):
    creado = PedidoService.crear_pedido(pedido)
    if creado is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear pedido")
    return creado


@router.put("/{pedido_id}", response_model=Pedido)
def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate):
    actualizado = PedidoService.actualizar_pedido(pedido_id, pedido)
    if actualizado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado o sin cambios")
    return actualizado


@router.delete("/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    ok = PedidoService.eliminar_pedido(pedido_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    return {"message": "Pedido eliminado"}
