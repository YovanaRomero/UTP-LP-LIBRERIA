from mysql.connector import Error
from ..database import db
from ..models import Categoria, CategoriaCreate, CategoriaUpdate


class CategoriaRepository:
    """Repository para acceso a datos de categorías."""

    @staticmethod
    def get_all():
        """Obtener todas las categorías de la base de datos."""
        connection = db.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT categoria_id, categoria_descripcion FROM categoria"
            cursor.execute(query)
            results = cursor.fetchall()

            categorias = []
            for row in results:
                categorias.append(Categoria(
                    categoria_id=row['categoria_id'],
                    categoria_descripcion=row['categoria_descripcion']
                ))
            return categorias
        except Error as e:
            print(f"Error al obtener categorías: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(categoria_id: int):
        """Obtener una categoría por ID."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT categoria_id, categoria_descripcion FROM categoria WHERE categoria_id = %s"
            cursor.execute(query, (categoria_id,))
            result = cursor.fetchone()

            if result:
                return Categoria(
                    categoria_id=result['categoria_id'],
                    categoria_descripcion=result['categoria_descripcion']
                )
            return None
        except Error as e:
            print(f"Error al obtener categoría: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(categoria: CategoriaCreate):
        """Crear una nueva categoría."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            query = "INSERT INTO categoria (categoria_guid, categoria_descripcion) VALUES (UUID(), %s)"
            cursor.execute(query, (categoria.categoria_descripcion,))
            connection.commit()

            categoria_id = cursor.lastrowid
            return Categoria(
                categoria_id=categoria_id,
                categoria_descripcion=categoria.categoria_descripcion
            )
        except Error as e:
            print(f"Error al crear categoría: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(categoria_id: int, categoria: CategoriaUpdate):
        """Actualizar una categoría existente."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()

            # Construir query dinámicamente basado en los campos proporcionados
            update_fields = []
            values = []

            if categoria.categoria_descripcion is not None:
                update_fields.append("categoria_descripcion = %s")
                values.append(categoria.categoria_descripcion)

            if not update_fields:
                return None  # No hay campos para actualizar

            values.append(categoria_id)
            query = f"UPDATE categoria SET {', '.join(update_fields)} WHERE categoria_id = %s"

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount == 0:
                return None

            # Obtener la categoría actualizada
            return CategoriaRepository.get_by_id(categoria_id)
        except Error as e:
            print(f"Error al actualizar categoría: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete(categoria_id: int):
        """Eliminar una categoría."""
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            query = "DELETE FROM categoria WHERE categoria_id = %s"
            cursor.execute(query, (categoria_id,))
            connection.commit()

            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar categoría: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
