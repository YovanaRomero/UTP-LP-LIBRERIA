from ..models import Producto, ProductoCreate, ProductoUpdate
from ..repositories import ProductoRepository


class ProductoService:
    """Servicio de lógica de negocio para productos."""

    @staticmethod
    def get_all_productos():
        """Obtener todos los productos."""
        return ProductoRepository.get_all()

    @staticmethod
    def get_producto_by_id(producto_id: int):
        """Obtener un producto por ID."""
        return ProductoRepository.get_by_id(producto_id)

    @staticmethod
    def create_producto(producto: ProductoCreate):
        """Crear un nuevo producto."""
        return ProductoRepository.create(producto)

    @staticmethod
    def update_producto(producto_id: int, producto: ProductoUpdate):
        """Actualizar un producto existente."""
        return ProductoRepository.update(producto_id, producto)

    @staticmethod
    def delete_producto(producto_id: int):
        """Eliminar un producto."""
        return ProductoRepository.delete(producto_id)
