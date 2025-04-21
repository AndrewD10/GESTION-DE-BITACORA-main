from datetime import datetime
from .errores import (
    FechaInvalidaError,
    RangoFechasInvalidoError,
    ReporteError,
    CamposVaciosError
)
import re
from .actividad import Actividad


class Bitacora:
    """
    Clase para gestionar las entradas de bitácora: agregar, consultar y generar reportes.
    """

    def __init__(self, db):
        """
        Inicializa una instancia de Bitacora.

        :param db: Objeto de base de datos que permite ejecutar consultas.
        """
        self.db = db

    def agregar_entrada(self, actividad):
        """
        Agrega una entrada de actividad a la bitácora.

        :param actividad: Objeto con atributos:
            - fecha
            - supervisor
            - descripcion
            - anexos
            - responsable
            - clima
        :raises CamposVaciosError: Si alguno de los campos obligatorios está vacío.
        :raises FechaInvalidaError: Si la fecha tiene formato incorrecto.
        """
        campos_requeridos = [actividad.fecha, actividad.supervisor, actividad.descripcion, actividad.responsable]
        if not all(campos_requeridos):
            raise CamposVaciosError()

        try:
            datetime.strptime(actividad.fecha, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()

        query = """
            INSERT INTO bitacora (fecha, supervisor, descripcion, anexos, responsable, clima)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            actividad.fecha,
            actividad.supervisor,
            actividad.descripcion,
            actividad.anexos,
            actividad.responsable,
            actividad.clima
        )
        self.db.execute_query(query, params)

    def obtener_entradas(self, fecha_inicio, fecha_fin):
        """
        Obtiene las entradas de la bitácora dentro de un rango de fechas.

        :param fecha_inicio: Fecha de inicio en formato YYYY-MM-DD.
        :param fecha_fin: Fecha de fin en formato YYYY-MM-DD.
        :return: Lista de registros obtenidos.
        :raises FechaInvalidaError: Si alguna fecha tiene formato incorrecto o está vacía.
        :raises RangoFechasInvalidoError: Si la fecha de inicio es posterior a la de fin.
        """
        if not fecha_inicio or not fecha_fin:
            raise FechaInvalidaError("Las fechas no pueden estar vacías.")

        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()

        if inicio > fin:
            raise RangoFechasInvalidoError("La fecha de inicio no puede ser mayor que la fecha de fin.")

        query = "SELECT * FROM bitacora WHERE fecha BETWEEN ? AND ?"
        params = (fecha_inicio, fecha_fin)
        return self.db.fetch_query(query, params)

    def generar_reporte(self, fecha_inicio, fecha_fin, archivo_pdf="reporte.pdf"):
        """
        Genera un reporte en PDF con las entradas de la bitácora entre dos fechas.

        :param fecha_inicio: Fecha de inicio (YYYY-MM-DD).
        :param fecha_fin: Fecha de fin (YYYY-MM-DD).
        :param archivo_pdf: Nombre del archivo PDF a generar.
        :return: True si se generó correctamente.
        :raises FechaInvalidaError: Si alguna fecha es inválida.
        :raises RangoFechasInvalidoError: Si las fechas están invertidas.
        :raises ReporteError: Si ocurre un error al escribir el archivo o si el nombre del archivo es inválido.
        """
        # Validar el nombre del archivo usando una expresión regular
        if not re.match(r"^[\w,\s-]+\.[A-Za-z]{3}$", archivo_pdf):  # Solo letras, números, guiones, espacios y extensión .pdf
            raise ReporteError("El nombre del archivo es inválido.")

        # Validar fechas
        if not fecha_inicio or not fecha_fin:
            raise FechaInvalidaError("Las fechas no pueden estar vacías.")

        if not archivo_pdf:
            raise ReporteError("El nombre del archivo no puede estar vacío.")

        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()

        if inicio > fin:
            raise RangoFechasInvalidoError("La fecha de inicio no puede ser mayor que la fecha de fin.")

        actividades = self.obtener_entradas(fecha_inicio, fecha_fin)

        try:
            with open(archivo_pdf, 'w', encoding='utf-8') as f:
                f.write("Reporte de actividades\n")
                if not actividades:
                    f.write("No hay actividades registradas en este rango de fechas.\n")
                else:
                    for actividad in actividades:
                        f.write(f"{actividad}\n")
        except Exception as e:
            raise ReporteError(f"No se pudo generar el reporte: {str(e)}")

        return True
