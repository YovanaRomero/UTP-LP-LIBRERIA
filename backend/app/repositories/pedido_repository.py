from mysql.connector import Error
from ..database import db
from ..models import Pedido, PedidoCreate, PedidoUpdate
from ..repositories.detalle_repository import DetalleRepository


class PedidoRepository:

    # ===========================
    # OBTENER TODOS LOS PEDIDOS
    # ===========================
    @staticmethod
    def get_all():
        connection = db.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT pedido_id, pedido_guid, pedido_numero, pedido_fecha_registro,
                       pedido_fecha_entrega, pedido_personal_delivery, pedido_observaciones,
                       cliente_cliente_id, pedido_subtotal, pedido_igv, pedido_total, pedido_estado
                FROM pedido
            """
            cursor.execute(query)
            results = cursor.fetchall()

            pedidos = []
            for row in results:
                pedido_obj = Pedido(**row)
                pedido_obj.detalles = DetalleRepository.get_by_pedido(pedido_obj.pedido_id)
                pedidos.append(pedido_obj)

            return pedidos

        except Error as e:
            print(f"Error al obtener pedidos: {e}")
            return []

        finally:
            cursor.close()

    # ===========================
    # OBTENER PEDIDO POR ID
    # ===========================
    @staticmethod
    def get_by_id(pedido_id: int):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT pedido_id, pedido_guid, pedido_numero, pedido_fecha_registro,
                       pedido_fecha_entrega, pedido_personal_delivery, pedido_observaciones,
                       cliente_cliente_id, pedido_subtotal, pedido_igv, pedido_total, pedido_estado
                FROM pedido
                WHERE pedido_id = %s
            """
            cursor.execute(query, (pedido_id,))
            row = cursor.fetchone()
            if row:
                pedido_obj = Pedido(**row)
                pedido_obj.detalles = DetalleRepository.get_by_pedido(pedido_obj.pedido_id)
                return pedido_obj
            return None

        except Error as e:
            print(f"Error al obtener pedido: {e}")
            return None

        finally:
            cursor.close()

    # ===========================
    # CREAR PEDIDO
    # ===========================
    @staticmethod
    def create(pedido: PedidoCreate):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO pedido (pedido_guid, pedido_numero, pedido_fecha_registro,
                                    pedido_fecha_entrega, pedido_personal_delivery, pedido_observaciones,
                                    cliente_cliente_id, pedido_subtotal, pedido_igv, pedido_total, pedido_estado)
                VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                pedido.pedido_numero,
                pedido.pedido_fecha_registro,
                pedido.pedido_fecha_entrega,
                pedido.pedido_personal_delivery,
                pedido.pedido_observaciones,
                pedido.cliente_cliente_id,
                pedido.pedido_subtotal,
                pedido.pedido_igv,
                pedido.pedido_total,
                pedido.pedido_estado,
            ))
            pedido_id = cursor.lastrowid

            # Crear detalles usando DetalleRepository
            detalles = getattr(pedido, 'detalles', [])
            for i, d in enumerate(detalles, start=1):
                DetalleRepository.create(pedido_id, d, i)

            connection.commit()
            return PedidoRepository.get_by_id(pedido_id)

        except Error as e:
            print(f"Error al crear pedido: {e}")
            connection.rollback()
            return None

        finally:
            cursor.close()

    # ===========================
    # ACTUALIZAR PEDIDO
    # ===========================
    @staticmethod
    def update(pedido_id: int, pedido: PedidoUpdate):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            update_fields = []
            values = []

            for field, value in pedido.dict(exclude_unset=True).items():
                update_fields.append(f"{field} = %s")
                values.append(value)

            if not update_fields:
                return None

            values.append(pedido_id)
            query = f"UPDATE pedido SET {', '.join(update_fields)} WHERE pedido_id = %s"
            cursor.execute(query, tuple(values))
            connection.commit()

            return PedidoRepository.get_by_id(pedido_id)

        except Error as e:
            print(f"Error al actualizar pedido: {e}")
            connection.rollback()
            return None

        finally:
            cursor.close()

    # ===========================
    # ELIMINAR PEDIDO
    # ===========================
    @staticmethod
    def delete(pedido_id: int):
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            # Primero eliminar detalles
            DetalleRepository.delete_all_of_pedido(pedido_id)
            # Luego eliminar pedido
            cursor.execute("DELETE FROM pedido WHERE pedido_id = %s", (pedido_id,))
            connection.commit()
            return cursor.rowcount > 0

        except Error as e:
            print(f"Error al eliminar pedido: {e}")
            connection.rollback()
            return False

        finally:
            cursor.close()