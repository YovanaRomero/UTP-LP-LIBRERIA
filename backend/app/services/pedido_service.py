from typing import Optional
from ..models import Pedido, PedidoCreate, PedidoUpdate
from ..repositories import PedidoRepository


class PedidoService:
    @staticmethod
    def listar_pedidos():
        return PedidoRepository.get_all()

    @staticmethod
    def obtener_pedido(pedido_id: int) -> Optional[Pedido]:
        return PedidoRepository.get_by_id(pedido_id)

    @staticmethod
    def crear_pedido(pedido: PedidoCreate) -> Optional[Pedido]:
        return PedidoRepository.create(pedido)

    @staticmethod
    def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate) -> Optional[Pedido]:
        return PedidoRepository.update(pedido_id, pedido)

    @staticmethod
    def eliminar_pedido(pedido_id: int) -> bool:
        return PedidoRepository.delete(pedido_id)
