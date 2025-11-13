from ..models import Cliente, ClienteCreate, ClienteUpdate
from ..repositories import ClienteRepository


class ClienteService:
    """Servicio de lógica de negocio para clientes."""

    @staticmethod
    def get_all_clientes():
        """Obtener todos los clientes."""
        return ClienteRepository.get_all()

    @staticmethod
    def get_cliente_by_id(cliente_id: int):
        """Obtener un cliente por ID."""
        return ClienteRepository.get_by_id(cliente_id)

    @staticmethod
    def create_cliente(cliente: ClienteCreate):
        """Crear un nuevo cliente."""
        return ClienteRepository.create(cliente)

    @staticmethod
    def update_cliente(cliente_id: int, cliente: ClienteUpdate):
        """Actualizar un cliente existente."""
        return ClienteRepository.update(cliente_id, cliente)

    @staticmethod
    def delete_cliente(cliente_id: int):
        """Eliminar un cliente."""
        return ClienteRepository.delete(cliente_id)
