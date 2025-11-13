from mysql.connector import Error
from ..database import db
from ..models import Pedido, PedidoCreate, PedidoUpdate
from ..models import DetalleCreate
from .detalle_repository import DetalleRepository


class PedidoRepository:
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
                pedido_obj = Pedido(
                    pedido_id=row['pedido_id'],
                    pedido_guid=row.get('pedido_guid'),
                    pedido_numero=row.get('pedido_numero'),
                    pedido_fecha_registro=row.get('pedido_fecha_registro'),
                    pedido_fecha_entrega=row.get('pedido_fecha_entrega'),
                    pedido_personal_delivery=row.get('pedido_personal_delivery'),
                    pedido_observaciones=row.get('pedido_observaciones'),
                    cliente_cliente_id=row['cliente_cliente_id'],
                    pedido_subtotal=row.get('pedido_subtotal'),
                    pedido_igv=row.get('pedido_igv'),
                    pedido_total=row.get('pedido_total'),
                    pedido_estado=row.get('pedido_estado')
                )
                # Obtener detalles asociados
                try:
                    detalles = DetalleRepository.get_by_pedido(pedido_obj.pedido_id)
                except Exception:
                    detalles = []
                pedido_obj.detalles = detalles
                pedidos.append(pedido_obj)
            return pedidos
        except Error as e:
            print(f"Error al obtener pedidos: {e}")
            return []
        finally:
            cursor.close()

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
                FROM pedido WHERE pedido_id = %s
            """
            cursor.execute(query, (pedido_id,))
            row = cursor.fetchone()
            if row:
                pedido_obj = Pedido(
                    pedido_id=row['pedido_id'],
                    pedido_guid=row.get('pedido_guid'),
                    pedido_numero=row.get('pedido_numero'),
                    pedido_fecha_registro=row.get('pedido_fecha_registro'),
                    pedido_fecha_entrega=row.get('pedido_fecha_entrega'),
                    pedido_personal_delivery=row.get('pedido_personal_delivery'),
                    pedido_observaciones=row.get('pedido_observaciones'),
                    cliente_cliente_id=row['cliente_cliente_id'],
                    pedido_subtotal=row.get('pedido_subtotal'),
                    pedido_igv=row.get('pedido_igv'),
                    pedido_total=row.get('pedido_total'),
                    pedido_estado=row.get('pedido_estado')
                )
                try:
                    pedido_obj.detalles = DetalleRepository.get_by_pedido(pedido_obj.pedido_id)
                except Exception:
                    pedido_obj.detalles = []
                return pedido_obj
            return None
        except Error as e:
            print(f"Error al obtener pedido: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(pedido: PedidoCreate):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            # Usar la misma conexión para operación transaccional (pedido + detalles)
            cursor = connection.cursor()
            query = """
                INSERT INTO pedido (pedido_guid, pedido_numero, pedido_fecha_registro,
                                    pedido_fecha_entrega, pedido_personal_delivery, pedido_observaciones,
                                    cliente_cliente_id, pedido_subtotal, pedido_igv, pedido_total, pedido_estado)
                VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

            # Insertar detalles si vienen en el payload
            detalles = getattr(pedido, 'detalles', None)
            if detalles:
                detalle_query = """
                    INSERT INTO detalle (detalle_pedido_id, detalle_producto_id, detalle_secuencia,
                                         detalle_producto_precio, detalle_cantidad)
                    VALUES (%s, %s, %s, %s, %s)
                """
                for d in detalles:
                    # d is DetalleCreate
                    cursor.execute(detalle_query, (
                        pedido_id,
                        d.detalle_producto_id,
                        d.detalle_secuencia,
                        d.detalle_producto_precio,
                        d.detalle_cantidad,
                    ))

            connection.commit()
            return PedidoRepository.get_by_id(pedido_id)
        except Error as e:
            print(f"Error al crear pedido: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(pedido_id: int, pedido: PedidoUpdate):
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            update_fields = []
            values = []

            if pedido.pedido_numero is not None:
                update_fields.append("pedido_numero = %s")
                values.append(pedido.pedido_numero)
            if pedido.pedido_fecha_registro is not None:
                update_fields.append("pedido_fecha_registro = %s")
                values.append(pedido.pedido_fecha_registro)
            if pedido.pedido_fecha_entrega is not None:
                update_fields.append("pedido_fecha_entrega = %s")
                values.append(pedido.pedido_fecha_entrega)
            if pedido.pedido_personal_delivery is not None:
                update_fields.append("pedido_personal_delivery = %s")
                values.append(pedido.pedido_personal_delivery)
            if pedido.pedido_observaciones is not None:
                update_fields.append("pedido_observaciones = %s")
                values.append(pedido.pedido_observaciones)
            if pedido.cliente_cliente_id is not None:
                update_fields.append("cliente_cliente_id = %s")
                values.append(pedido.cliente_cliente_id)
            if pedido.pedido_subtotal is not None:
                update_fields.append("pedido_subtotal = %s")
                values.append(pedido.pedido_subtotal)
            if pedido.pedido_igv is not None:
                update_fields.append("pedido_igv = %s")
                values.append(pedido.pedido_igv)
            if pedido.pedido_total is not None:
                update_fields.append("pedido_total = %s")
                values.append(pedido.pedido_total)
            if pedido.pedido_estado is not None:
                update_fields.append("pedido_estado = %s")
                values.append(pedido.pedido_estado)

            if not update_fields:
                return None

            values.append(pedido_id)
            query = f"UPDATE pedido SET {', '.join(update_fields)} WHERE pedido_id = %s"
            cursor.execute(query, tuple(values))
            connection.commit()

            if cursor.rowcount == 0:
                return None
            return PedidoRepository.get_by_id(pedido_id)
        except Error as e:
            print(f"Error al actualizar pedido: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete(pedido_id: int):
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            query = "DELETE FROM pedido WHERE pedido_id = %s"
            cursor.execute(query, (pedido_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar pedido: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
