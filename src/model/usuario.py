from .errores import CamposVaciosError, UsuarioNoEncontradoError, ContrasenaIncorrectaError, CorreoYaRegistradoError
import re

class Usuario:
    """
    Clase que representa a un usuario en el sistema.

    :param db: Objeto de la base de datos que se utilizará para realizar consultas.
    """
    def __init__(self, db):
        self.db = db
    
    def crear_cuenta(self, nombre, correo, contrasena):
        """
        Crea una nueva cuenta de usuario.

        :param nombre: Nombre del usuario.
        :param correo: Correo electrónico del usuario.
        :param contrasena: Contraseña del usuario.
        
        :raises CamposVaciosError: Si alguno de los campos es vacío.
        :raises CorreoYaRegistradoError: Si el correo ya está registrado.
        """
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        if not re.match(patron_correo, correo.strip()):
            raise CamposVaciosError("Formato de correo inválido.")

        # Validar longitud mínima de la contraseña
        if len(contrasena.strip()) < 6:
            raise CamposVaciosError("La contraseña es muy corta.")

        query = "SELECT * FROM usuarios WHERE correo = ?"
        if self.db.fetch_query(query, (correo.strip(),)):
            raise CorreoYaRegistradoError()

        query = "INSERT INTO usuarios (nombre, correo, contrasena) VALUES (?, ?, ?)"
        self.db.execute_query(query, (nombre.strip(), correo.strip(), contrasena.strip()))
        return True
    
    def iniciar_sesion(self, correo, contrasena):
        """
        Inicia sesión con el correo y la contraseña del usuario.

        :param correo: Correo electrónico del usuario.
        :param contrasena: Contraseña del usuario.
        
        :raises CamposVaciosError: Si el correo o la contraseña están vacíos.
        :raises UsuarioNoEncontradoError: Si no se encuentra el usuario con el correo proporcionado.
        :raises ContrasenaIncorrectaError: Si la contraseña es incorrecta.
        
        :return: Datos del usuario si la sesión es exitosa.
        """
        if not correo or not contrasena:
            raise CamposVaciosError()

        query = "SELECT * FROM usuarios WHERE correo = ?"
        usuario = self.db.fetch_query(query, (correo,))
        if not usuario:
            raise UsuarioNoEncontradoError()

        if usuario[0][3] != contrasena:
            raise ContrasenaIncorrectaError()

        return usuario[0]
    
    def cambiar_contrasena(self, correo, nueva_contrasena):
        """
        Cambia la contraseña de un usuario.

        :param correo: Correo electrónico del usuario.
        :param nueva_contrasena: Nueva contraseña del usuario.
        
        :raises CamposVaciosError: Si el correo o la nueva contraseña están vacíos.
        :raises UsuarioNoEncontradoError: Si no se encuentra el usuario con el correo proporcionado.
        :raises ValueError: Si la nueva contraseña es igual a la anterior.
        
        :return: True si la contraseña se actualiza correctamente.
        """
        if not correo or not nueva_contrasena:
            raise CamposVaciosError("El correo y la nueva contraseña no pueden estar vacíos.")

        query = "SELECT * FROM usuarios WHERE correo = ?"
        usuario = self.db.fetch_query(query, (correo.strip(),))
        if not usuario:
            raise UsuarioNoEncontradoError()

        if usuario[0][3] == nueva_contrasena.strip():
            raise ValueError("La nueva contraseña no puede ser igual a la anterior.")

        query = "UPDATE usuarios SET contrasena = ? WHERE correo = ?"
        params = (nueva_contrasena.strip(), correo.strip())
        self.db.execute_query(query, params)
        return True
