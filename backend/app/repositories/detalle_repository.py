from mysql.connector import Error
from ..database import db
from ..models import Detalle, DetalleCreate, DetalleUpdate


class DetalleRepository:

    # ===========================
    # OBTENER DETALLES POR PEDIDO
    # ===========================
    @staticmethod
    def get_by_pedido(pedido_id: int):
        connection = db.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT detalle_pedido_id, detalle_producto_id, detalle_secuencia,
                       detalle_producto_precio, detalle_cantidad
                FROM detalle
                WHERE detalle_pedido_id = %s
                ORDER BY detalle_secuencia ASC
            """
            cursor.execute(query, (pedido_id,))
            rows = cursor.fetchall()

            return [Detalle(**r) for r in rows]

        except Error as e:
            print(f"Error al obtener detalles: {e}")
            return []

        finally:
            cursor.close()

    # ===========================
    # CREAR DETALLE
    # ===========================
    @staticmethod
    def create(pedido_id: int, detalle: DetalleCreate, secuencia: int):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO detalle (detalle_pedido_id, detalle_producto_id, detalle_secuencia,
                                     detalle_producto_precio, detalle_cantidad)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                pedido_id,
                detalle.detalle_producto_id,
                secuencia,
                detalle.detalle_producto_precio,
                detalle.detalle_cantidad
            ))
            connection.commit()
            return True

        except Error as e:
            print(f"Error al crear detalle: {e}")
            connection.rollback()
            return False

        finally:
            cursor.close()

    # ===========================
    # ELIMINAR TODOS LOS DETALLES DE UN PEDIDO
    # ===========================
    @staticmethod
    def delete_all_of_pedido(pedido_id: int):
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM detalle WHERE detalle_pedido_id = %s", (pedido_id,))
            connection.commit()
            return True

        except Error as e:
            print(f"Error al eliminar detalles: {e}")
            connection.rollback()
            return False

        finally:
            cursor.close()

    # ===========================
    # ACTUALIZAR DETALLE
    # ===========================
    @staticmethod
    def update(pedido_id: int, producto_id: int, detalle: DetalleUpdate):
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            update_fields = []
            values = []

            if detalle.detalle_secuencia is not None:
                update_fields.append("detalle_secuencia = %s")
                values.append(detalle.detalle_secuencia)

            if detalle.detalle_producto_precio is not None:
                update_fields.append("detalle_producto_precio = %s")
                values.append(detalle.detalle_producto_precio)

            if detalle.detalle_cantidad is not None:
                update_fields.append("detalle_cantidad = %s")
                values.append(detalle.detalle_cantidad)

            if not update_fields:
                return False

            values.extend([pedido_id, producto_id])
            query = f"""
                UPDATE detalle
                SET {', '.join(update_fields)}
                WHERE detalle_pedido_id = %s AND detalle_producto_id = %s
            """
            cursor.execute(query, tuple(values))
            connection.commit()
            return cursor.rowcount > 0

        except Error as e:
            print(f"Error al actualizar detalle: {e}")
            connection.rollback()
            return False

        finally:
            cursor.close()

    # ===========================
    # ELIMINAR DETALLE ESPECÍFICO
    # ===========================
    @staticmethod
    def delete(pedido_id: int, producto_id: int):
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            query = """
                DELETE FROM detalle
                WHERE detalle_pedido_id = %s AND detalle_producto_id = %s
            """
            cursor.execute(query, (pedido_id, producto_id))
            connection.commit()
            return cursor.rowcount > 0

        except Error as e:
            print(f"Error al eliminar detalle: {e}")
            connection.rollback()
            return False

        finally:
            cursor.close()