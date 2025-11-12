from mysql.connector import Error
from .database import db
from .models import Categoria, CategoriaCreate, CategoriaUpdate


class CategoriaService:
    @staticmethod
    def get_all_categorias():
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
    def get_categoria_by_id(categoria_id: int):
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
    def create_categoria(categoria: CategoriaCreate):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            query = "INSERT INTO categoria (categoria_guid,categoria_descripcion) VALUES (UUID(),%s)"
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
    def update_categoria(categoria_id: int, categoria: CategoriaUpdate):
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
            return CategoriaService.get_categoria_by_id(categoria_id)
        except Error as e:
            print(f"Error al actualizar categoría: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete_categoria(categoria_id: int):
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