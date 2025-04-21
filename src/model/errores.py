class BaseError(Exception):
    """Clase base para los errores personalizados."""
    pass

class CamposVaciosError(BaseError):
    """
    Se genera cuando un campo obligatorio está vacío.

    :param mensaje: Mensaje personalizado del error.
    """
    def __init__(self, mensaje="Los campos no pueden estar vacíos."):
        super().__init__(mensaje)

class UsuarioNoEncontradoError(BaseError):
    """
    Se genera cuando un usuario no existe en la base de datos.

    :param mensaje: Mensaje personalizado del error.
    """
    def __init__(self, mensaje="El usuario no existe."):
        super().__init__(mensaje)

class ContrasenaIncorrectaError(BaseError):
    """
    Se genera cuando la contraseña ingresada es incorrecta.

    :param mensaje: Mensaje personalizado del error.
    """
    def __init__(self, mensaje="Contraseña incorrecta."):
        super().__init__(mensaje)

class CorreoYaRegistradoError(BaseError):
    """
    Se genera cuando se intenta registrar un usuario con un correo ya existente.

    :param mensaje: Mensaje personalizado del error.
    """
    def __init__(self, mensaje="El correo ya está registrado."):
        super().__init__(mensaje)

class FechaInvalidaError(BaseError):
    """
    Se genera cuando se ingresa una fecha con formato incorrecto.

    :param mensaje: Mensaje personalizado del error.
    """
    def __init__(self, mensaje="La fecha ingresada no es válida."):
        super().__init__(mensaje)

class RangoFechasInvalidoError(BaseError):
    """
    Se genera cuando el rango de fechas ingresado no es válido.

    :param mensaje: Mensaje personalizado del error.
    """
    def __init__(self, mensaje="El rango de fechas es inválido."):
        super().__init__(mensaje)

class ReporteError(BaseError):
    """
    Se genera cuando hay un problema al generar el reporte.

    :param mensaje: Mensaje personalizado del error.
    """
    def __init__(self, mensaje="No se pudo generar el reporte."):
        super().__init__(mensaje)
