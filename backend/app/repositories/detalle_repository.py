from mysql.connector import Error
from ..database import db
from ..models import Detalle, DetalleCreate, DetalleUpdate


class DetalleRepository:
    @staticmethod
    def get_by_pedido(detalle_pedido_id: int):
        connection = db.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT detalle_pedido_id, detalle_producto_id, detalle_secuencia,
                       detalle_producto_precio, detalle_cantidad
                FROM detalle WHERE detalle_pedido_id = %s
            """
            cursor.execute(query, (detalle_pedido_id,))
            rows = cursor.fetchall()

            detalles = []
            for r in rows:
                detalles.append(Detalle(
                    detalle_pedido_id=r['detalle_pedido_id'],
                    detalle_producto_id=r['detalle_producto_id'],
                    detalle_secuencia=r.get('detalle_secuencia'),
                    detalle_producto_precio=r.get('detalle_producto_precio'),
                    detalle_cantidad=r.get('detalle_cantidad')
                ))
            return detalles
        except Error as e:
            print(f"Error al obtener detalles: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def create(detalle_pedido_id: int, detalle: DetalleCreate):
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
                detalle_pedido_id,
                detalle.detalle_producto_id,
                detalle.detalle_secuencia,
                detalle.detalle_producto_precio,
                detalle.detalle_cantidad,
            ))
            connection.commit()
            return DetalleRepository.get_by_pedido(detalle_pedido_id)
        except Error as e:
            print(f"Error al crear detalle: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(detalle_pedido_id: int, detalle_producto_id: int, detalle: DetalleUpdate):
        connection = db.get_connection()
        if connection is None:
            return None

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
                return None

            values.extend([detalle_pedido_id, detalle_producto_id])
            query = f"UPDATE detalle SET {', '.join(update_fields)} WHERE detalle_pedido_id = %s AND detalle_producto_id = %s"
            cursor.execute(query, tuple(values))
            connection.commit()

            if cursor.rowcount == 0:
                return None
            return DetalleRepository.get_by_pedido(detalle_pedido_id)
        except Error as e:
            print(f"Error al actualizar detalle: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete(detalle_pedido_id: int, detalle_producto_id: int):
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            query = "DELETE FROM detalle WHERE detalle_pedido_id = %s AND detalle_producto_id = %s"
            cursor.execute(query, (detalle_pedido_id, detalle_producto_id))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar detalle: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
