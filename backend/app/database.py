import mysql.connector
from mysql.connector import Error
from .config import settings


class Database:
    def __init__(self):
        # Usar settings centralizados
        self.host = settings.DB_HOST
        self.database = settings.DB_NAME
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.port = settings.DB_PORT
        self.connection = None

    def get_connection(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
                print("Conexión a MySQL establecida correctamente")
            return self.connection
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a MySQL cerrada")

# Instancia global de la base de datos
db = Database()