from mysql.connector import Error
import time
from ..database import db
from ..models import Producto, ProductoCreate, ProductoUpdate


class ProductoRepository:
    """Repository para acceso a datos de productos."""

    # ==========================
    # LISTAR TODOS
    # ==========================
    @staticmethod
    def get_all():
        connection = db.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT p.producto_id, p.producto_guid, p.producto_serie, p.producto_nombre, 
                       p.producto_descripcion, p.producto_precio, p.producto_stock, 
                       p.producto_color, p.producto_dimensiones, p.producto_estado, 
                       p.categoria_categoria_id, c.categoria_descripcion AS categoria_categoria_descripcion
                FROM producto p
                INNER JOIN categoria c ON p.categoria_categoria_id = c.categoria_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            productos = []
            for r in rows:
                productos.append(Producto(
                    producto_id=r['producto_id'],
                    producto_guid=r.get('producto_guid'),
                    producto_serie=r.get('producto_serie'),
                    producto_nombre=r.get('producto_nombre'),
                    producto_descripcion=r.get('producto_descripcion'),
                    producto_precio=r.get('producto_precio'),
                    producto_stock=r.get('producto_stock'),
                    producto_color=r.get('producto_color'),
                    producto_dimensiones=r.get('producto_dimensiones'),
                    producto_estado=r.get('producto_estado'),
                    categoria_categoria_id=r.get('categoria_categoria_id'),
                    categoria_categoria_descripcion=r.get('categoria_categoria_descripcion')
                ))
            return productos

        except Error as e:
            print(f"Error al obtener productos: {e}")
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

    # ==========================
    # OBTENER PRODUCTO POR ID
    # ==========================
    @staticmethod
    def get_by_id(producto_id: int):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT producto_id, producto_guid, producto_serie, producto_nombre, 
                       producto_descripcion, producto_precio, producto_stock, 
                       producto_color, producto_dimensiones, producto_estado, 
                       categoria_categoria_id 
                FROM producto 
                WHERE producto_id = %s
            """
            cursor.execute(query, (producto_id,))
            r = cursor.fetchone()

            if r:
                return Producto(
                    producto_id=r['producto_id'],
                    producto_guid=r['producto_guid'],
                    producto_serie=r['producto_serie'],
                    producto_nombre=r['producto_nombre'],
                    producto_descripcion=r['producto_descripcion'],
                    producto_precio=r['producto_precio'],
                    producto_stock=r['producto_stock'],
                    producto_color=r['producto_color'],
                    producto_dimensiones=r['producto_dimensiones'],
                    producto_estado=r['producto_estado'],
                    categoria_categoria_id=r['categoria_categoria_id']
                )
            return None

        except Error as e:
            print(f"Error al obtener producto: {e}")
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

    # ==========================
    # VALIDAR STOCK
    # ==========================
    @staticmethod
    def validar_stock(producto_id: int, cantidad_solicitada: int):
        producto = ProductoRepository.get_by_id(producto_id)

        if producto is None:
            return False, "Producto no existe"

        if producto.producto_estado == 0:
            return False, "Producto inactivo"

        if producto.producto_stock < cantidad_solicitada:
            return False, "Stock insuficiente"

        return True, producto.producto_stock

    # ==========================
    # DESCONTAR STOCK
    # ==========================
    @staticmethod
    def descontar_stock(producto_id: int, cantidad: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()

            query = """
                UPDATE producto
                SET producto_stock = producto_stock - %s
                WHERE producto_id = %s
                AND producto_stock >= %s
            """
            cursor.execute(query, (cantidad, producto_id, cantidad))
            connection.commit()

            return cursor.rowcount > 0

        except Error as e:
            print(f"Error al descontar stock: {e}")
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

    # ==========================
    # RESTAURAR STOCK (si se elimina un pedido/detalle)
    # ==========================
    @staticmethod
    def restaurar_stock(producto_id: int, cantidad: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()

            query = """
                UPDATE producto
                SET producto_stock = producto_stock + %s
                WHERE producto_id = %s
            """
            cursor.execute(query, (cantidad, producto_id))
            connection.commit()

            return cursor.rowcount > 0

        except Error as e:
            print(f"Error al restaurar stock: {e}")
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

    # ==========================
    # CREAR PRODUCTO
    # ==========================
    @staticmethod
    def create(producto: ProductoCreate):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO producto (
                    producto_guid, producto_serie, producto_nombre, 
                    producto_descripcion, producto_precio, producto_stock,
                    producto_color, producto_dimensiones, producto_estado,
                    categoria_categoria_id
                )
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
            return ProductoRepository.get_by_id(cursor.lastrowid)

        except Error as e:
            print(f"Error al crear producto: {e}")
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

    # ==========================
    # ACTUALIZAR PRODUCTO
    # ==========================
    @staticmethod
    def update(producto_id: int, producto: ProductoUpdate):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            start = time.time()
            cursor = connection.cursor(dictionary=True)
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
                return None

            values.append(producto_id)

            query = f"""
                UPDATE producto
                SET {', '.join(update_fields)}
                WHERE producto_id = %s
            """

            # execute update and commit
            # Ensure session lock wait timeout is low to fail fast on contention
            try:
                cursor.execute("SET SESSION innodb_lock_wait_timeout = %s", (5,))
            except Exception:
                pass
            exec_start = time.time()
            cursor.execute(query, tuple(values))
            connection.commit()
            exec_end = time.time()

            # Log timings for diagnosis
            total_elapsed = time.time() - start
            exec_elapsed = exec_end - exec_start
            print(f"[producto.update] exec_elapsed={exec_elapsed:.4f}s total_elapsed={total_elapsed:.4f}s query=" + query)

            # Fetch the updated row using the same connection (avoid opening a new connection)
            try:
                cursor.execute("""
                    SELECT producto_id, producto_guid, producto_serie, producto_nombre, 
                           producto_descripcion, producto_precio, producto_stock, 
                           producto_color, producto_dimensiones, producto_estado, 
                           categoria_categoria_id 
                    FROM producto 
                    WHERE producto_id = %s
                """, (producto_id,))
                r = cursor.fetchone()
                if r:
                    return Producto(
                        producto_id=r['producto_id'],
                        producto_guid=r['producto_guid'],
                        producto_serie=r['producto_serie'],
                        producto_nombre=r['producto_nombre'],
                        producto_descripcion=r['producto_descripcion'],
                        producto_precio=r['producto_precio'],
                        producto_stock=r['producto_stock'],
                        producto_color=r['producto_color'],
                        producto_dimensiones=r['producto_dimensiones'],
                        producto_estado=r['producto_estado'],
                        categoria_categoria_id=r['categoria_categoria_id']
                    )
            except Exception as e:
                print(f"[producto.update] error fetching updated row: {e}")
            return ProductoRepository.get_by_id(producto_id)

        except Error as e:
            print(f"Error al actualizar producto: {e}")
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

    # ==========================
    # ELIMINAR PRODUCTO
    # ==========================
    @staticmethod
    def delete(producto_id: int):
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
            try:
                cursor.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass

    @staticmethod
    def get_stock_productos():
        """Obtiene el stock de cada producto (nombre y cantidad)."""
        connection = db.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                    SELECT producto_nombre, producto_stock
                    FROM producto
                    ORDER BY producto_stock ASC
                """
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error al obtener stock de productos: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
