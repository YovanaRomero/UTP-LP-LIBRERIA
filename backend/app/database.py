import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', '173.249.41.159')
        self.database = os.getenv('DB_NAME', 'salesdb')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'my801521my')
        self.port = os.getenv('DB_PORT', '3306')
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