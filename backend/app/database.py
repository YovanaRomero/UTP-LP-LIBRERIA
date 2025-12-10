import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from .config import settings


class Database:
    def __init__(self):
        # Usar settings centralizados
        self.host = settings.DB_HOST
        self.database = settings.DB_NAME
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.port = settings.DB_PORT
        self.pool = None
        self._init_pool()

    def _init_pool(self):
        try:
            # pool_size configurable desde settings
            pool_size = getattr(settings, 'DB_POOL_SIZE', 10)
            self.pool = pooling.MySQLConnectionPool(
                pool_name="utp_pool",
                pool_size=pool_size,
                pool_reset_session=True,
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            print(f"Pool de conexiones MySQL inicializado (size={pool_size})")
        except Error as e:
            print(f"Error al crear pool de conexiones MySQL: {e}")
            self.pool = None

    def get_connection(self):
        try:
            if self.pool is None:
                self._init_pool()
            if self.pool is None:
                return None
            # Devuelve una conexión del pool (el caller debe cerrarla para devolverla al pool)
            conn = self.pool.get_connection()
            # Aplicar ajustes de sesión para evitar esperas largas por locks
            try:
                cursor = conn.cursor()
                lock_timeout = getattr(settings, 'DB_LOCK_WAIT_TIMEOUT', 5)
                # innodb_lock_wait_timeout controla cuánto espera una transacción por bloqueos
                cursor.execute("SET SESSION innodb_lock_wait_timeout = %s", (lock_timeout,))
                cursor.close()
            except Exception as e:
                # No detener la obtención de conexión si no se pudo aplicar el ajuste
                print(f"Warning: no se pudo aplicar innodb_lock_wait_timeout: {e}")
            return conn
        except Error as e:
            print(f"Error al obtener conexión del pool: {e}")
            return None

    def close_pool(self):
        # No existe un close explícito para el pool en mysql-connector; dejamos que GC maneje.
        self.pool = None


# Instancia global de la base de datos
db = Database()