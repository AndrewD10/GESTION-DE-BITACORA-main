import psycopg2

conn = psycopg2.connect(
    dbname="bitacorina_db",
    user="postgres",
    password="maxelo31hd",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Lista de sentencias SQL
sentencias_sql = [
    """
    CREATE TABLE usuarios (
        id_usuario SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        correo VARCHAR(150) UNIQUE NOT NULL,
        contraseña VARCHAR(255) NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE bitacoras (
        id_bitacora SERIAL PRIMARY KEY,
        id_usuario INT NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        descripcion TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_bitacoras_usuario FOREIGN KEY (id_usuario)
            REFERENCES usuarios(id_usuario)
            ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE actividades (
        id_actividad SERIAL PRIMARY KEY,
        id_bitacora INT NOT NULL,
        fecha DATE NOT NULL,
        descripcion TEXT NOT NULL,
        anexos TEXT,
        responsable VARCHAR(100),
        clima VARCHAR(50),
        estado VARCHAR(50),
        tipo VARCHAR(50),
        CONSTRAINT fk_actividades_bitacora FOREIGN KEY (id_bitacora)
            REFERENCES bitacoras(id_bitacora)
            ON DELETE CASCADE
    );
    """
]

# Ejecutar cada sentencia por separado
for sentencia in sentencias_sql:
    cur.execute(sentencia)

conn.commit()
cur.close()
conn.close()

print("Tablas creadas correctamente.")
