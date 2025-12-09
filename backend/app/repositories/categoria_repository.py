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
            query = "SELECT categoria_id, categoria_guid, categoria_nombre, categoria_descripcion, categoria_estado FROM categoria"
            cursor.execute(query)
            results = cursor.fetchall()

            categorias = []
            for row in results:
                categorias.append(Categoria(
                    categoria_id=row['categoria_id'],
                    categoria_guid=row['categoria_guid'],
                    categoria_nombre=row['categoria_nombre'],
                    categoria_descripcion=row['categoria_descripcion'],
                    categoria_estado= row['categoria_estado']
                ))
            return categorias
        except Error as e:
            print(f"Error al obtener categorías: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass

    @staticmethod
    def get_by_id(categoria_id: int):
        """Obtener una categoría por ID."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT categoria_id, categoria_guid, categoria_nombre, categoria_descripcion, categoria_estado FROM categoria WHERE categoria_id = %s"
            cursor.execute(query, (categoria_id,))
            result = cursor.fetchone()

            if result:
                return Categoria(
                    categoria_id=result['categoria_id'],
                    categoria_guid=result['categoria_guid'],
                    categoria_nombre=result['categoria_nombre'],
                    categoria_descripcion=result['categoria_descripcion'],
                    categoria_estado=result['categoria_estado']
                )
            return None
        except Error as e:
            print(f"Error al obtener categoría: {e}")
            return None
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass

    @staticmethod
    def create(categoria: CategoriaCreate):
        """Crear una nueva categoría."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            query = "INSERT INTO categoria (categoria_guid, categoria_nombre, categoria_descripcion, categoria_estado) VALUES (UUID(), %s, %s, %s)"
            cursor.execute(query, (
                categoria.categoria_nombre,
                categoria.categoria_descripcion,
                categoria.categoria_estado
            ))
            connection.commit()

            categoria_id = cursor.lastrowid
            return CategoriaRepository.get_by_id(categoria_id)
        except Error as e:
            print(f"Error al crear categoría: {e}")
            connection.rollback()
            return None
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass

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

            if categoria.categoria_nombre is not None:
                update_fields.append("categoria_nombre = %s")
                values.append(categoria.categoria_nombre)

            if categoria.categoria_descripcion is not None:
                update_fields.append("categoria_descripcion = %s")
                values.append(categoria.categoria_descripcion)

            if categoria.categoria_estado is not None:
                update_fields.append("categoria_estado = %s")
                values.append(categoria.categoria_estado)

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
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass

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
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass
