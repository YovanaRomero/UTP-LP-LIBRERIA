from mysql.connector import Error
from ..database import db
from ..models import Producto, ProductoCreate, ProductoUpdate


class ProductoRepository:
    """Repository para acceso a datos de productos."""

    @staticmethod
    def get_all():
        """Obtener todos los productos de la base de datos."""
        connection = db.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT producto_id, producto_nombre, producto_descripcion, 
                       producto_precio, categoria_id FROM producto
            """
            cursor.execute(query)
            results = cursor.fetchall()

            productos = []
            for row in results:
                productos.append(Producto(
                    producto_id=row['producto_id'],
                    producto_nombre=row['producto_nombre'],
                    producto_descripcion=row['producto_descripcion'],
                    producto_precio=row['producto_precio'],
                    categoria_id=row['categoria_id']
                ))
            return productos
        except Error as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(producto_id: int):
        """Obtener un producto por ID."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT producto_id, producto_nombre, producto_descripcion, 
                       producto_precio, categoria_id FROM producto WHERE producto_id = %s
            """
            cursor.execute(query, (producto_id,))
            result = cursor.fetchone()

            if result:
                return Producto(
                    producto_id=result['producto_id'],
                    producto_nombre=result['producto_nombre'],
                    producto_descripcion=result['producto_descripcion'],
                    producto_precio=result['producto_precio'],
                    categoria_id=result['categoria_id']
                )
            return None
        except Error as e:
            print(f"Error al obtener producto: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(producto: ProductoCreate):
        """Crear un nuevo producto."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO producto (producto_nombre, producto_descripcion, 
                                     producto_precio, categoria_id) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                producto.producto_nombre,
                producto.producto_descripcion,
                producto.producto_precio,
                producto.categoria_id
            ))
            connection.commit()

            producto_id = cursor.lastrowid
            return Producto(
                producto_id=producto_id,
                producto_nombre=producto.producto_nombre,
                producto_descripcion=producto.producto_descripcion,
                producto_precio=producto.producto_precio,
                categoria_id=producto.categoria_id
            )
        except Error as e:
            print(f"Error al crear producto: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(producto_id: int, producto: ProductoUpdate):
        """Actualizar un producto existente."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()

            # Construir query dinámicamente basado en los campos proporcionados
            update_fields = []
            values = []

            if producto.producto_nombre is not None:
                update_fields.append("producto_nombre = %s")
                values.append(producto.producto_nombre)

            if producto.producto_descripcion is not None:
                update_fields.append("producto_descripcion = %s")
                values.append(producto.producto_descripcion)

            if producto.producto_precio is not None:
                update_fields.append("producto_precio = %s")
                values.append(producto.producto_precio)

            if producto.categoria_id is not None:
                update_fields.append("categoria_id = %s")
                values.append(producto.categoria_id)

            if not update_fields:
                return None  # No hay campos para actualizar

            values.append(producto_id)
            query = f"UPDATE producto SET {', '.join(update_fields)} WHERE producto_id = %s"

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount == 0:
                return None

            # Obtener el producto actualizado
            return ProductoRepository.get_by_id(producto_id)
        except Error as e:
            print(f"Error al actualizar producto: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete(producto_id: int):
        """Eliminar un producto."""
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            query = "DELETE FROM producto WHERE producto_id = %s"
            cursor.execute(query, (producto_id,))
            connection.commit()

            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar producto: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
