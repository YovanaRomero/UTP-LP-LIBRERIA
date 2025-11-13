from ..models import Categoria, CategoriaCreate, CategoriaUpdate
from ..repositories import CategoriaRepository


class CategoriaService:
    """Servicio de lógica de negocio para categorías."""

    @staticmethod
    def get_all_categorias():
        """Obtener todas las categorías."""
        return CategoriaRepository.get_all()

    @staticmethod
    def get_categoria_by_id(categoria_id: int):
        """Obtener una categoría por ID."""
        return CategoriaRepository.get_by_id(categoria_id)

    @staticmethod
    def create_categoria(categoria: CategoriaCreate):
        """Crear una nueva categoría."""
        return CategoriaRepository.create(categoria)

    @staticmethod
    def update_categoria(categoria_id: int, categoria: CategoriaUpdate):
        """Actualizar una categoría existente."""
        return CategoriaRepository.update(categoria_id, categoria)

    @staticmethod
    def delete_categoria(categoria_id: int):
        """Eliminar una categoría."""
        return CategoriaRepository.delete(categoria_id)
