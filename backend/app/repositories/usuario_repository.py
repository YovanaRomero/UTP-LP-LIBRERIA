from mysql.connector import Error
from ..database import db
from ..models import Usuario


class UsuarioRepository:
    """Repository para acceso a datos de usuarios."""

    @staticmethod
    def get_by_nombre(usuario_nombre: str):
        """Obtener un usuario por nombre."""
        connection = db.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT usuario_id, usuario_guid, usuario_nombre, usuario_descripcion, 
                       usuario_password, usuario_estado FROM usuario WHERE usuario_nombre = %s
            """
            cursor.execute(query, (usuario_nombre,))
            result = cursor.fetchone()

            if result:
                return {
                    "usuario_id": result['usuario_id'],
                    "usuario_guid": result['usuario_guid'],
                    "usuario_nombre": result['usuario_nombre'],
                    "usuario_descripcion": result['usuario_descripcion'],
                    "usuario_password": result['usuario_password'],
                    "usuario_estado": result['usuario_estado']
                }
            return None
        except Error as e:
            print(f"Error al obtener usuario por nombre: {e}")
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
