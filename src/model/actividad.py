from .errores import CamposVaciosError, FechaInvalidaError, RangoFechasInvalidoError
from datetime import datetime

class Actividad:
    """
    Clase encargada de gestionar el registro, consulta y generación de reportes de actividades.
    """

    def __init__(self, db):
        """
        Inicializa una instancia de Actividad.

        :param db: Instancia de la base de datos para ejecutar consultas.
        """
        self.db = db

    def registrar_actividad(self, datos_actividad):
        """
        Registra una nueva actividad en la base de datos.

        :param datos_actividad: Diccionario con los campos:
            - fecha
            - supervisor
            - descripcion
            - anexos
            - responsable
            - clima
        :raises CamposVaciosError: Si falta alguno de los campos obligatorios.
        :raises FechaInvalidaError: Si la fecha tiene un formato incorrecto.
        """
        # Validar que los campos obligatorios estén presentes en el diccionario
        campos_obligatorios = ['fecha', 'supervisor', 'descripcion', 'responsable']
        for campo in campos_obligatorios:
            if not datos_actividad.get(campo):
                raise CamposVaciosError()

        # Validar que la fecha tenga el formato correcto
        try:
            datetime.strptime(datos_actividad['fecha'].strip(), "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()

        # Realizar la consulta de inserción en la base de datos
        query = """
            INSERT INTO actividades (fecha, supervisor, descripcion, anexos, responsable, clima)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            datos_actividad['fecha'].strip(),
            datos_actividad['supervisor'].strip(),
            datos_actividad['descripcion'].strip(),
            datos_actividad.get('anexos', '').strip(),
            datos_actividad['responsable'].strip(),
            datos_actividad.get('clima', '').strip()
        )
        self.db.execute_query(query, params)

    def consultar_actividades(self, fecha_inicio, fecha_fin):
        """
        Consulta las actividades registradas en un rango de fechas.

        :param fecha_inicio: Fecha de inicio en formato YYYY-MM-DD.
        :param fecha_fin: Fecha de fin en formato YYYY-MM-DD.
        :return: Lista de actividades encontradas.
        :raises FechaInvalidaError: Si alguna fecha no es válida.
        :raises RangoFechasInvalidoError: Si la fecha de inicio es posterior a la fecha de fin.
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

        query = "SELECT * FROM actividades WHERE fecha BETWEEN ? AND ?"
        params = (fecha_inicio, fecha_fin)
        return self.db.fetch_query(query, params)

    def generar_reporte(self, fecha_inicio, fecha_fin, archivo_pdf="reporte.pdf"):
        """
        Genera un archivo PDF con las actividades entre dos fechas.

        :param fecha_inicio: Fecha de inicio del reporte (YYYY-MM-DD).
        :param fecha_fin: Fecha de fin del reporte (YYYY-MM-DD).
        :param archivo_pdf: Nombre del archivo PDF de salida.
        :return: True si el reporte se generó correctamente.
        :raises FechaInvalidaError: Si las fechas no son válidas.
        :raises RangoFechasInvalidoError: Si la fecha de inicio es mayor a la de fin.
        :raises ValueError: Si el archivo no se puede crear.
        """
        if not fecha_inicio or not fecha_fin:
            raise FechaInvalidaError("Las fechas no pueden estar vacías.")

        if not archivo_pdf:
            raise ValueError("El nombre del archivo no puede estar vacío.")

        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()

        if inicio > fin:
            raise RangoFechasInvalidoError("La fecha de inicio no puede ser mayor que la fecha de fin.")

        actividades = self.consultar_actividades(fecha_inicio, fecha_fin)

        try:
            with open(archivo_pdf, 'w', encoding='utf-8') as f:
                f.write("Reporte de actividades\n")
                if not actividades:
                    f.write("No hay actividades registradas en este rango de fechas.\n")
                else:
                    for actividad in actividades:
                        f.write(f"{actividad}\n")
        except Exception as e:
            raise ValueError(f"Error al generar el reporte: {str(e)}")

        return True
