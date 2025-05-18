from .errores import CamposVaciosError, FechaInvalidaError, RangoFechasInvalidoError
from datetime import datetime
from src.model.orm_model import ActividadORM, Session


class Actividad:
    def __init__(self, db=None):
        self.db = db  # No se usa directamente si usamos ORM

    """
    Clase encargada de gestionar el registro, consulta y generación de reportes de actividades.
    """

    def registrar_actividad(self, datos_actividad):
        """
        Registra una nueva actividad en la base de datos usando SQLAlchemy ORM.

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

        # Validar formato de la fecha
        try:
            fecha_obj = datetime.strptime(datos_actividad['fecha'].strip(), "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()

        # Registrar la actividad usando SQLAlchemy ORM
        session = Session()
        try:
            nueva_actividad = ActividadORM(
                fecha=fecha_obj.date(),
                supervisor=datos_actividad['supervisor'].strip(),
                descripcion=datos_actividad['descripcion'].strip(),
                anexos=datos_actividad.get('anexos', '').strip(),
                responsable=datos_actividad['responsable'].strip(),
                clima=datos_actividad.get('clima', '').strip()
            )
            session.add(nueva_actividad)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def consultar_actividades(self, fecha_inicio, fecha_fin):
        """
        Consulta las actividades registradas en un rango de fechas usando SQLAlchemy ORM
        y devuelve los resultados como una lista de diccionarios.

        :param fecha_inicio: Fecha de inicio en formato YYYY-MM-DD.
        :param fecha_fin: Fecha de fin en formato YYYY-MM-DD.
        :return: Lista de diccionarios con los datos de las actividades.
        :raises FechaInvalidaError: Si alguna fecha no es válida.
        :raises RangoFechasInvalidoError: Si la fecha de inicio es posterior a la fecha de fin.
        """
    # Validar que ambas fechas estén presentes
        if not fecha_inicio or not fecha_fin:
            raise FechaInvalidaError("Las fechas no pueden estar vacías.")

    # Convertir cadenas a objetos de fecha
        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            raise FechaInvalidaError("Formato de fecha inválido.")

    # Validar que el rango de fechas sea lógico
        if inicio > fin:
            raise RangoFechasInvalidoError("La fecha de inicio no puede ser mayor que la fecha de fin.")

    # Crear sesión y consultar actividades dentro del rango
        session = Session()
        try:
            actividades = (
                session.query(ActividadORM)
                .filter(ActividadORM.fecha >= inicio, ActividadORM.fecha <= fin)
                .order_by(ActividadORM.fecha)
                .all()
            )

        # Convertir cada objeto ORM en un diccionario para facilitar el acceso en tests
            actividades_dict = [
                {
                    "id_actividad": a.id_actividad,
                    "fecha": a.fecha,
                    "descripcion": a.descripcion,
                    "anexos": a.anexos,
                    "responsable": a.responsable,
                    "clima": a.clima,
                    "estado": a.estado,
                    "tipo": a.tipo
                }
                for a in actividades
            ]
            return actividades_dict
        finally:
            session.close()


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

        # Obtener actividades con ORM
        actividades = self.consultar_actividades(fecha_inicio, fecha_fin)

        # Generar el archivo PDF simulando escritura a archivo de texto
        try:
            with open(archivo_pdf, 'w', encoding='utf-8') as f:
                f.write("Reporte de actividades\n")
                if not actividades:
                    f.write("No hay actividades registradas en este rango de fechas.\n")
                else:
                    for act in actividades:
                        f.write(
                            f"{act.fecha} | {act.supervisor} | {act.descripcion} | {act.anexos or ''} | {act.responsable} | {act.clima or ''}\n"
                        )
        except Exception as e:
            raise ValueError(f"Error al generar el reporte: {str(e)}")

        return True
