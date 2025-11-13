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
                SELECT producto_id, producto_guid, producto_serie, producto_nombre, 
                       producto_descripcion, producto_precio, producto_stock, 
                       producto_color, producto_dimensiones, producto_estado, 
                       categoria_categoria_id FROM producto
            """
            cursor.execute(query)
            results = cursor.fetchall()

            productos = []
            for row in results:
                productos.append(Producto(
                    producto_id=row['producto_id'],
                    producto_guid=row['producto_guid'],
                    producto_serie=row['producto_serie'],
                    producto_nombre=row['producto_nombre'],
                    producto_descripcion=row['producto_descripcion'],
                    producto_precio=row['producto_precio'],
                    producto_stock=row['producto_stock'],
                    producto_color=row['producto_color'],
                    producto_dimensiones=row['producto_dimensiones'],
                    producto_estado=row['producto_estado'],
                    categoria_categoria_id=row['categoria_categoria_id']
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
                SELECT producto_id, producto_guid, producto_serie, producto_nombre, 
                       producto_descripcion, producto_precio, producto_stock, 
                       producto_color, producto_dimensiones, producto_estado, 
                       categoria_categoria_id FROM producto WHERE producto_id = %s
            """
            cursor.execute(query, (producto_id,))
            result = cursor.fetchone()

            if result:
                return Producto(
                    producto_id=result['producto_id'],
                    producto_guid=result['producto_guid'],
                    producto_serie=result['producto_serie'],
                    producto_nombre=result['producto_nombre'],
                    producto_descripcion=result['producto_descripcion'],
                    producto_precio=result['producto_precio'],
                    producto_stock=result['producto_stock'],
                    producto_color=result['producto_color'],
                    producto_dimensiones=result['producto_dimensiones'],
                    producto_estado=result['producto_estado'],
                    categoria_categoria_id=result['categoria_categoria_id']
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
                INSERT INTO producto (producto_guid, producto_serie, producto_nombre, 
                                     producto_descripcion, producto_precio, producto_stock, 
                                     producto_color, producto_dimensiones, producto_estado, 
                                     categoria_categoria_id) 
                VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                producto.producto_serie,
                producto.producto_nombre,
                producto.producto_descripcion,
                producto.producto_precio,
                producto.producto_stock,
                producto.producto_color,
                producto.producto_dimensiones,
                producto.producto_estado,
                producto.categoria_categoria_id
            ))
            connection.commit()

            producto_id = cursor.lastrowid
            return ProductoRepository.get_by_id(producto_id)
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

            if producto.producto_stock is not None:
                update_fields.append("producto_stock = %s")
                values.append(producto.producto_stock)

            if producto.producto_color is not None:
                update_fields.append("producto_color = %s")
                values.append(producto.producto_color)

            if producto.producto_dimensiones is not None:
                update_fields.append("producto_dimensiones = %s")
                values.append(producto.producto_dimensiones)

            if producto.producto_estado is not None:
                update_fields.append("producto_estado = %s")
                values.append(producto.producto_estado)

            if producto.categoria_categoria_id is not None:
                update_fields.append("categoria_categoria_id = %s")
                values.append(producto.categoria_categoria_id)

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
