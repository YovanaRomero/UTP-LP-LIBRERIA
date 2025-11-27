from mysql.connector import Error
from ..database import db
from ..models import Cliente, ClienteCreate, ClienteUpdate


class ClienteRepository:
    """Repository para acceso a datos de clientes."""

    @staticmethod
    def get_all():
        """Obtener todos los clientes de la base de datos."""
        connection = db.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT cliente_id, cliente_guid, cliente_dni, cliente_nombres, 
                       cliente_apellidos, cliente_direccion, cliente_distrito, 
                       cliente_correo, cliente_celular, cliente_estado FROM cliente
            """
            cursor.execute(query)
            results = cursor.fetchall()

            clientes = []
            for row in results:
                clientes.append(Cliente(
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
                ))
            return clientes
        except Error as e:
            print(f"Error al obtener clientes: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(cliente_id: int):
        """Obtener un cliente por ID."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT cliente_id, cliente_guid, cliente_dni, cliente_nombres, 
                       cliente_apellidos, cliente_direccion, cliente_distrito, 
                       cliente_correo, cliente_celular, cliente_estado FROM cliente 
                WHERE cliente_id = %s
            """
            cursor.execute(query, (cliente_id,))
            result = cursor.fetchone()

            if result:
                return Cliente(
                    cliente_id=result['cliente_id'],
                    cliente_guid=result['cliente_guid'],
                    cliente_dni=result['cliente_dni'],
                    cliente_nombres=result['cliente_nombres'],
                    cliente_apellidos=result['cliente_apellidos'],
                    cliente_direccion=result['cliente_direccion'],
                    cliente_distrito=result['cliente_distrito'],
                    cliente_correo=result['cliente_correo'],
                    cliente_celular=result['cliente_celular'],
                    cliente_estado=result['cliente_estado']
                )
            return None
        except Error as e:
            print(f"Error al obtener cliente: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(cliente: ClienteCreate):
        """Crear un nuevo cliente."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO cliente (cliente_guid, cliente_dni, cliente_nombres, 
                                    cliente_apellidos, cliente_direccion, cliente_distrito, 
                                    cliente_correo, cliente_celular, cliente_estado) 
                VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                cliente.cliente_dni,
                cliente.cliente_nombres,
                cliente.cliente_apellidos,
                cliente.cliente_direccion,
                cliente.cliente_distrito,
                cliente.cliente_correo,
                cliente.cliente_celular,
                cliente.cliente_estado
            ))
            connection.commit()

            cliente_id = cursor.lastrowid
            return ClienteRepository.get_by_id(cliente_id)
        except Error as e:
            print(f"Error al crear cliente: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def update(cliente_id: int, cliente: ClienteUpdate):
        """Actualizar un cliente existente."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()

            # Construir query dinámicamente basado en los campos proporcionados
            update_fields = []
            values = []

            if cliente.cliente_dni is not None:
                update_fields.append("cliente_dni = %s")
                values.append(cliente.cliente_dni)

            if cliente.cliente_nombres is not None:
                update_fields.append("cliente_nombres = %s")
                values.append(cliente.cliente_nombres)

            if cliente.cliente_apellidos is not None:
                update_fields.append("cliente_apellidos = %s")
                values.append(cliente.cliente_apellidos)

            if cliente.cliente_direccion is not None:
                update_fields.append("cliente_direccion = %s")
                values.append(cliente.cliente_direccion)

            if cliente.cliente_distrito is not None:
                update_fields.append("cliente_distrito = %s")
                values.append(cliente.cliente_distrito)

            if cliente.cliente_correo is not None:
                update_fields.append("cliente_correo = %s")
                values.append(cliente.cliente_correo)

            if cliente.cliente_celular is not None:
                update_fields.append("cliente_celular = %s")
                values.append(cliente.cliente_celular)

            if cliente.cliente_estado is not None:
                update_fields.append("cliente_estado = %s")
                values.append(cliente.cliente_estado)

            if not update_fields:
                return None  # No hay campos para actualizar

            values.append(cliente_id)
            query = f"UPDATE cliente SET {', '.join(update_fields)} WHERE cliente_id = %s"

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount == 0:
                return None

            # Obtener el cliente actualizado
            return ClienteRepository.get_by_id(cliente_id)
        except Error as e:
            print(f"Error al actualizar cliente: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete(cliente_id: int):
        """Eliminar un cliente."""
        connection = db.get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            query = "DELETE FROM cliente WHERE cliente_id = %s"
            cursor.execute(query, (cliente_id,))
            connection.commit()

            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar cliente: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
