from mysql.connector import Error
from ..database import db
from ..models import Pedido, PedidoCreate, PedidoUpdate
from ..repositories.detalle_repository import DetalleRepository
from ..repositories.cliente_repository import ClienteRepository
from datetime import datetime


def _format_datetime(value):
    """Convierte datetime a string YYYY-MM-DD HH:MM:SS, o devuelve None si es nulo"""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


class PedidoRepository:

    # ===========================
    # OBTENER TODOS LOS PEDIDOS
    # ===========================
    @staticmethod
    def get_all():
        connection = db.get_connection()
        if connection is None:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            # JOIN con cliente para traer datos completos del cliente en una sola query
            query = """
                SELECT p.pedido_id, p.pedido_guid, p.pedido_numero, p.pedido_fecha_registro,
                       p.pedido_fecha_entrega, p.pedido_personal_delivery, p.pedido_observaciones,
                       p.cliente_cliente_id, p.pedido_subtotal, p.pedido_igv, p.pedido_total, p.pedido_estado,
                       c.cliente_id, c.cliente_guid, c.cliente_dni, c.cliente_nombres, 
                       c.cliente_apellidos, c.cliente_direccion, c.cliente_distrito, 
                       c.cliente_correo, c.cliente_celular, c.cliente_estado
                FROM pedido p
                LEFT JOIN cliente c ON p.cliente_cliente_id = c.cliente_id
                ORDER BY p.pedido_id DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()

            pedidos = []
            for row in results:
                pedido_obj = Pedido(
                    pedido_id=row['pedido_id'],
                    pedido_guid=row['pedido_guid'],
                    pedido_numero=row['pedido_numero'],
                    pedido_fecha_registro=_format_datetime(row['pedido_fecha_registro']),
                    pedido_fecha_entrega=_format_datetime(row['pedido_fecha_entrega']),
                    pedido_personal_delivery=row['pedido_personal_delivery'],
                    pedido_observaciones=row['pedido_observaciones'],
                    cliente_cliente_id=row['cliente_cliente_id'],
                    pedido_subtotal=row['pedido_subtotal'],
                    pedido_igv=row['pedido_igv'],
                    pedido_total=row['pedido_total'],
                    pedido_estado=row['pedido_estado']
                )
                
                # Asignar cliente directamente desde los datos del JOIN
                if row['cliente_id']:
                    from ..models import Cliente
                    pedido_obj.cliente = Cliente(
                        cliente_id=row['cliente_id'],
                        cliente_guid=row['cliente_guid'],
                        cliente_dni=row['cliente_dni'],
                        cliente_nombres=row['cliente_nombres'],
                        cliente_apellidos=row['cliente_apellidos'],
                        cliente_direccion=row['cliente_direccion'],
                        cliente_distrito=row['cliente_distrito'],
                        cliente_correo=row['cliente_correo'],
                        cliente_celular=row['cliente_celular'],
                        cliente_estado=row['cliente_estado']
                    )
                
                # Obtener detalles (N queries, pero es necesario para la estructura actual)
                pedido_obj.detalles = DetalleRepository.get_by_pedido(pedido_obj.pedido_id)
                pedidos.append(pedido_obj)

            return pedidos

        except Error as e:
            print(f"Error al obtener pedidos: {e}")
            return []

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

    # ===========================
    # OBTENER TODOS LOS PEDIDOS (LIGHTWEIGHT - sin detalles)
    # ===========================
    @staticmethod
    def get_all_lightweight():
        """
        Obtiene todos los pedidos con datos del cliente, SIN detalles.
        Mucho más rápido para listados que get_all().
        Usa esta si solo necesitas mostrar una tabla de pedidos sin expandir detalles.
        """
        connection = db.get_connection()
        if connection is None:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT p.pedido_id, p.pedido_guid, p.pedido_numero, p.pedido_fecha_registro,
                       p.pedido_fecha_entrega, p.pedido_personal_delivery, p.pedido_observaciones,
                       p.cliente_cliente_id, p.pedido_subtotal, p.pedido_igv, p.pedido_total, p.pedido_estado,
                       c.cliente_id, c.cliente_guid, c.cliente_dni, c.cliente_nombres, 
                       c.cliente_apellidos, c.cliente_direccion, c.cliente_distrito, 
                       c.cliente_correo, c.cliente_celular, c.cliente_estado
                FROM pedido p
                LEFT JOIN cliente c ON p.cliente_cliente_id = c.cliente_id
                ORDER BY p.pedido_id DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()

            pedidos = []
            for row in results:
                pedido_obj = Pedido(
                    pedido_id=row['pedido_id'],
                    pedido_guid=row['pedido_guid'],
                    pedido_numero=row['pedido_numero'],
                    pedido_fecha_registro=_format_datetime(row['pedido_fecha_registro']),
                    pedido_fecha_entrega=_format_datetime(row['pedido_fecha_entrega']),
                    pedido_personal_delivery=row['pedido_personal_delivery'],
                    pedido_observaciones=row['pedido_observaciones'],
                    cliente_cliente_id=row['cliente_cliente_id'],
                    pedido_subtotal=row['pedido_subtotal'],
                    pedido_igv=row['pedido_igv'],
                    pedido_total=row['pedido_total'],
                    pedido_estado=row['pedido_estado']
                )
                
                # Asignar cliente directamente
                if row['cliente_id']:
                    from ..models import Cliente
                    pedido_obj.cliente = Cliente(
                        cliente_id=row['cliente_id'],
                        cliente_guid=row['cliente_guid'],
                        cliente_dni=row['cliente_dni'],
                        cliente_nombres=row['cliente_nombres'],
                        cliente_apellidos=row['cliente_apellidos'],
                        cliente_direccion=row['cliente_direccion'],
                        cliente_distrito=row['cliente_distrito'],
                        cliente_correo=row['cliente_correo'],
                        cliente_celular=row['cliente_celular'],
                        cliente_estado=row['cliente_estado']
                    )
                
                pedidos.append(pedido_obj)

            return pedidos

        except Error as e:
            print(f"Error al obtener pedidos (lightweight): {e}")
            return []

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

    # ===========================
    # OBTENER PEDIDO POR ID
    # ===========================
    @staticmethod
    def get_by_id(pedido_id: int):
        connection = db.get_connection()
        if connection is None:
            return None

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            # JOIN con cliente para traer datos completos en una sola query
            query = """
                SELECT p.pedido_id, p.pedido_guid, p.pedido_numero, p.pedido_fecha_registro,
                       p.pedido_fecha_entrega, p.pedido_personal_delivery, p.pedido_observaciones,
                       p.cliente_cliente_id, p.pedido_subtotal, p.pedido_igv, p.pedido_total, p.pedido_estado,
                       c.cliente_id, c.cliente_guid, c.cliente_dni, c.cliente_nombres, 
                       c.cliente_apellidos, c.cliente_direccion, c.cliente_distrito, 
                       c.cliente_correo, c.cliente_celular, c.cliente_estado
                FROM pedido p
                LEFT JOIN cliente c ON p.cliente_cliente_id = c.cliente_id
                WHERE p.pedido_id = %s
            """
            cursor.execute(query, (pedido_id,))
            row = cursor.fetchone()
            
            if row:
                pedido_obj = Pedido(
                    pedido_id=row['pedido_id'],
                    pedido_guid=row['pedido_guid'],
                    pedido_numero=row['pedido_numero'],
                    pedido_fecha_registro=_format_datetime(row['pedido_fecha_registro']),
                    pedido_fecha_entrega=_format_datetime(row['pedido_fecha_entrega']),
                    pedido_personal_delivery=row['pedido_personal_delivery'],
                    pedido_observaciones=row['pedido_observaciones'],
                    cliente_cliente_id=row['cliente_cliente_id'],
                    pedido_subtotal=row['pedido_subtotal'],
                    pedido_igv=row['pedido_igv'],
                    pedido_total=row['pedido_total'],
                    pedido_estado=row['pedido_estado']
                )
                
                # Asignar cliente directamente desde los datos del JOIN
                if row['cliente_id']:
                    from ..models import Cliente
                    pedido_obj.cliente = Cliente(
                        cliente_id=row['cliente_id'],
                        cliente_guid=row['cliente_guid'],
                        cliente_dni=row['cliente_dni'],
                        cliente_nombres=row['cliente_nombres'],
                        cliente_apellidos=row['cliente_apellidos'],
                        cliente_direccion=row['cliente_direccion'],
                        cliente_distrito=row['cliente_distrito'],
                        cliente_correo=row['cliente_correo'],
                        cliente_celular=row['cliente_celular'],
                        cliente_estado=row['cliente_estado']
                    )
                
                # Obtener detalles
                pedido_obj.detalles = DetalleRepository.get_by_pedido(pedido_obj.pedido_id)
                return pedido_obj
            return None

        except Error as e:
            print(f"Error al obtener pedido: {e}")
            return None

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

    # ===========================
    # CREAR PEDIDO
    # ===========================
    @staticmethod
    def create(pedido: PedidoCreate):
        connection = db.get_connection()
        if connection is None:
            return None

        cursor = None
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
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

    # ===========================
    # ACTUALIZAR PEDIDO
    # ===========================
    @staticmethod
    def update(pedido_id: int, pedido: PedidoUpdate):
        connection = db.get_connection()
        if connection is None:
            return None

        cursor = None
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
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

    # ===========================
    # ELIMINAR PEDIDO
    # ===========================
    @staticmethod
    def delete(pedido_id: int):
        connection = db.get_connection()
        if connection is None:
            return False

        cursor = None
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
            if cursor:
                cursor.close()
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass