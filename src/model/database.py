import sqlite3

class Database:
    """
    Clase para gestionar la conexión y consultas a la base de datos.
    """

    def __init__(self, db_name="bitacora.db"):
        """
        Inicializa la conexión a la base de datos.

        :param db_name: Nombre de la base de datos (por defecto 'bitacora.db').
        """
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.
        """
        queries = [
            """
            CREATE TABLE IF NOT EXISTS bitacora (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                supervisor TEXT,
                descripcion TEXT,
                anexos TEXT,
                responsable TEXT,
                clima TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS actividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                supervisor TEXT,
                descripcion TEXT,
                anexos TEXT,
                responsable TEXT,
                clima TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                correo TEXT UNIQUE,
                contrasena TEXT
            )
            """
        ]
        for query in queries:
            self.execute_query(query)

    def execute_query(self, query, params=()):
        """
        Ejecuta una consulta que modifica la base de datos (INSERT, UPDATE, DELETE).

        :param query: Consulta SQL a ejecutar.
        :param params: Parámetros para la consulta.
        :return: El cursor de la consulta ejecutada.
        """
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor

    def fetch_query(self, query, params=()):
        """
        Ejecuta una consulta SELECT que recupera datos de la base de datos.

        :param query: Consulta SQL a ejecutar.
        :param params: Parámetros para la consulta.
        :return: Lista de resultados obtenidos.
        """
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return results if results else []

    def clear_tables(self):
        """
        Elimina todos los datos de las tablas sin eliminar la estructura de las mismas.
        """
        queries = [
            "DELETE FROM bitacora",
            "DELETE FROM actividades",
            "DELETE FROM usuarios"
        ]
        for query in queries:
            self.execute_query(query)
        self.connection.commit()

    def close_connection(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.connection.close()
