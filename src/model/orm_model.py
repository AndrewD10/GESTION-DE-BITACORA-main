from sqlalchemy import Column, Integer, String, Date, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False, unique=True)
    contraseña = Column(String(255), nullable=False)

class ActividadORM(Base):  # <- nombre corregido aquí
    __tablename__ = 'actividades'
    id_actividad = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=False)
    anexos = Column(Text)
    responsable = Column(String(100))
    clima = Column(String(50))
    estado = Column(String(50))
    tipo = Column(String(50))
    supervisor = Column(String(100))  

# Crear engine y sesión
engine = create_engine("sqlite:///actividades.db")  # o el de PostgreSQL
Session = sessionmaker(bind=engine)
