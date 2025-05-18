import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Configuración de conexión a PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bitacorina_db"
DB_USER = "postgres"
DB_PASSWORD = "maxelo31hd"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Clase para operaciones genéricas en base de datos
class Database:
    def execute_query(self, query, params=None):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                conn.commit()

    def fetch_query(self, query, params=None):
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params or ())
                return cur.fetchall()
    
    def clear_tables(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                TRUNCATE TABLE actividades, usuarios
                RESTART IDENTITY CASCADE;
            """)
            conn.commit()



# Funciones específicas para gestión de usuarios
def obtener_usuario_por_correo(correo):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM usuarios WHERE correo = %s;
            """, (correo,))
            return cur.fetchone()

def crear_usuario(nombre, correo, contrasena):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usuarios (nombre, correo, contrasena)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (nombre, correo, contrasena))
            return cur.fetchone()[0]

def autenticar_usuario(correo, contrasena):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM usuarios
                WHERE correo = %s AND contrasena = %s;
            """, (correo, contrasena))
            return cur.fetchone()

def actualizar_contrasena(correo, nueva_contrasena):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE usuarios SET contrasena = %s WHERE correo = %s;
            """, (nueva_contrasena, correo))

# Funciones específicas para actividades
def registrar_actividad(usuario_id, descripcion):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO actividades (usuario_id, descripcion, fecha)
                VALUES (%s, %s, %s);
            """, (usuario_id, descripcion, datetime.now()))

def obtener_actividades(usuario_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM actividades
                WHERE usuario_id = %s
                ORDER BY fecha DESC;
            """, (usuario_id,))
            return cur.fetchall()

# Funciones específicas para transacciones
def registrar_transaccion(usuario_id, cantidad, categoria, tipo):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO transacciones (usuario_id, cantidad, categoria, tipo, fecha)
                VALUES (%s, %s, %s, %s, %s);
            """, (usuario_id, cantidad, categoria, tipo, datetime.now()))

def obtener_transacciones(usuario_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM transacciones
                WHERE usuario_id = %s
                ORDER BY fecha DESC;
            """, (usuario_id,))
            return cur.fetchall()

def insertar_actividad(fecha, supervisor, descripcion, anexos, responsable, clima):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO actividades (fecha, supervisor, descripcion, anexos, responsable, clima)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (fecha, supervisor, descripcion, anexos, responsable, clima))
            conn.commit()

def obtener_actividades_por_rango(fecha_inicio, fecha_fin):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM actividades
                WHERE fecha BETWEEN %s AND %s
                ORDER BY fecha;
            """, (fecha_inicio, fecha_fin))
            return cur.fetchall()
        
