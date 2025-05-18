import re
from src.model import database
from .errores import CamposVaciosError, UsuarioNoEncontradoError, ContrasenaIncorrectaError, CorreoYaRegistradoError

class Usuario:
    def __init__(self, db):
        self.db = db
    
    def crear_cuenta(self, nombre, correo, contrasena):
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        if not re.match(patron_correo, correo.strip()):
            raise CamposVaciosError("Formato de correo inválido.")
        if len(contrasena.strip()) < 6:
            raise CamposVaciosError("La contraseña es muy corta.")

        # Verifica si ya existe el correo usando la función obtener_usuario_por_correo
        if database.obtener_usuario_por_correo(correo.strip()):
            raise CorreoYaRegistradoError()

        # Crea el usuario usando crear_usuario
        database.crear_usuario(nombre.strip(), correo.strip(), contrasena.strip())
        return True
    
    def iniciar_sesion(self, correo, contrasena):
        if not correo or not contrasena:
            raise CamposVaciosError()

        usuario = database.obtener_usuario_por_correo(correo.strip())
        if not usuario:
            raise UsuarioNoEncontradoError()

        if usuario['contrasena'] != contrasena:
            raise ContrasenaIncorrectaError()

        return usuario
    
    def cambiar_contrasena(self, correo, nueva_contrasena):
        if not correo or not nueva_contrasena:
            raise CamposVaciosError("El correo y la nueva contraseña no pueden estar vacíos.")

        usuario = database.obtener_usuario_por_correo(correo.strip())
        if not usuario:
            raise UsuarioNoEncontradoError()

        if usuario['contrasena'] == nueva_contrasena.strip():
            raise ValueError("La nueva contraseña no puede ser igual a la anterior.")

        # Aquí llamas a una función para actualizar la contraseña, como no la tienes, 
        # podemos agregarla en database.py o hacer la consulta aquí mismo:
        # Te dejo una función auxiliar simple aquí:

        database.actualizar_contrasena(correo.strip(), nueva_contrasena.strip())
        return True
