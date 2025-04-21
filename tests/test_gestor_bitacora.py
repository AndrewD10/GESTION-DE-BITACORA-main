import pytest
from src.model.actividad import Actividad
from src.model.bitacora import Bitacora
from src.model.usuario import Usuario
from src.model.database import Database
from src.model.errores import CamposVaciosError, FechaInvalidaError, RangoFechasInvalidoError, UsuarioNoEncontradoError, ContrasenaIncorrectaError, CorreoYaRegistradoError, ReporteError


class TestRegistroActividad:
    def setup_method(self, method):
        """Método de configuración para cada prueba"""
        self.db = Database()
        self.db.clear_tables()
        self.actividad = Actividad(self.db)
    
    # ---- PRUEBAS NORMALES ----
    def test_registro_actividad_valida(self):
        """Registrar una actividad con datos correctos"""
        self.actividad.registrar_actividad({
            "fecha": "2025-03-06",
            "supervisor": "Juan Pérez",
            "descripcion": "Revisión de equipos",
            "anexos": "anexo.pdf",
            "responsable": "María",
            "clima": "Soleado"
        })
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert len(actividades) == 1
    
    def test_registro_actividad_sin_anexo(self):
        """Registrar una actividad sin archivo adjunto"""
        self.actividad.registrar_actividad({
            "fecha": "2025-03-06",
            "supervisor": "Juan Pérez",
            "descripcion": "Limpieza del área",
            "anexos": "",
            "responsable": "Carlos",
            "clima": "Nublado"
        })
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert actividades[0][3] == "Limpieza del área"
    
    def test_registro_actividad_con_clima_variable(self):
        """Registrar una actividad con una condición climática cambiante"""
        self.actividad.registrar_actividad({
            "fecha": "2025-03-06",
            "supervisor": "Juan Pérez",
            "descripcion": "Reparación de equipo",
            "anexos": "",
            "responsable": "Ana",
            "clima": "Lluvia intermitente"
        })
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert actividades[0][6] == "Lluvia intermitente"
    
    # ---- PRUEBAS EXTREMAS ----
    def test_registro_actividad_fecha_lejana(self):
        """Registrar una actividad con una fecha muy en el futuro"""
        self.actividad.registrar_actividad({
            "fecha": "2035-12-31",
            "supervisor": "Juan Pérez",
            "descripcion": "Mantenimiento futuro",
            "anexos": "",
            "responsable": "Carlos",
            "clima": "Soleado"
        })
        actividades = self.actividad.consultar_actividades("2035-12-31", "2035-12-31")
        assert len(actividades) == 1
    
    def test_registro_actividad_mucha_info(self):
        """Registrar una actividad con una descripción muy larga"""
        descripcion_larga = "A" * 1000
        self.actividad.registrar_actividad({
            "fecha": "2025-03-06",
            "supervisor": "Juan Pérez",
            "descripcion": descripcion_larga,
            "anexos": "",
            "responsable": "Ana",
            "clima": "Nublado"
        })
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert len(actividades[0][3]) == 1000
    
    def test_registro_actividad_clima_desconocido(self):
        """Registrar una actividad con un tipo de clima poco común"""
        self.actividad.registrar_actividad({
            "fecha": "2025-03-06",
            "supervisor": "Juan Pérez",
            "descripcion": "Tarea de prueba",
            "anexos": "",
            "responsable": "Luis",
            "clima": "Huracán categoría 5"
        })
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert actividades[0][6] == "Huracán categoría 5"
    
    # ---- PRUEBAS DE ERROR ----
    def test_registro_actividad_fecha_invalida(self):
        """Intentar registrar una actividad con una fecha incorrecta"""
        with pytest.raises(FechaInvalidaError):
            self.actividad.registrar_actividad({
                "fecha": "fecha_invalida",
                "supervisor": "Juan Pérez",
                "descripcion": "Revisión",
                "anexos": "",
                "responsable": "Pedro",
                "clima": "Soleado"
            })
    
    def test_registro_actividad_sin_descripcion(self):
        """Intentar registrar una actividad sin descripción"""
        with pytest.raises(CamposVaciosError):
            self.actividad.registrar_actividad({
                "fecha": "2025-03-06",
                "supervisor": "Juan Pérez",
                "descripcion": "",
                "anexos": "",
                "responsable": "María",
                "clima": "Nublado"
            })
    
    def test_registro_actividad_sin_responsable(self):
        """Intentar registrar una actividad sin responsable asignado"""
        with pytest.raises(CamposVaciosError):
            self.actividad.registrar_actividad({
                "fecha": "2025-03-06",
                "supervisor": "Juan Pérez",
                "descripcion": "Reparación",
                "anexos": "",
                "responsable": "",
                "clima": "Soleado"
            })

class TestConsultarActividades:

    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.db.clear_tables()
        self.actividad = Actividad(self.db)
    
    # ---- PRUEBAS NORMALES ----
    def test_consultar_actividades_rango_valido(self):
        """Consultar actividades dentro de un rango de fechas válido"""
        resultado = self.actividad.consultar_actividades("2025-03-01", "2025-03-10")
        assert isinstance(resultado, list)
    
    def test_consultar_actividades_sin_resultados(self):
        """Consultar actividades en un rango donde no hay registros"""
        resultado = self.actividad.consultar_actividades("2030-01-01", "2030-01-10")
        assert resultado == []
    
    def test_consultar_actividades_fecha_actual(self):
        """Consultar actividades en la fecha actual"""
        resultado = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert isinstance(resultado, list)
    
    # ---- PRUEBAS EXTREMAS ----
    def test_consultar_actividades_rango_extremadamente_amplio(self):
        """Consultar actividades en un rango de fechas muy amplio"""
        resultado = self.actividad.consultar_actividades("2000-01-01", "2100-12-31")
        assert isinstance(resultado, list)
    
    def test_consultar_actividades_mismo_dia(self):
        """Consultar actividades en un solo día"""
        resultado = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert isinstance(resultado, list)
    
    def test_consultar_actividades_fechas_invertidas(self):
        """Consultar actividades con fechas invertidas (fecha fin antes que fecha inicio)"""
        with pytest.raises(RangoFechasInvalidoError):
            self.actividad.consultar_actividades("2025-03-10", "2025-03-01")
    
    # ---- PRUEBAS DE ERROR ----
    def test_consultar_actividades_fechas_invalidas(self):
        """Intentar consultar actividades con fechas inválidas"""
        with pytest.raises(FechaInvalidaError):
            self.actividad.consultar_actividades("fecha_invalida", "2025-03-06")
    
    def test_consultar_actividades_sin_parametros(self):
        """Intentar consultar actividades sin proporcionar fechas"""
        with pytest.raises(FechaInvalidaError):
            self.actividad.consultar_actividades("", "")
    
    def test_consultar_actividades_caracteres_especiales(self):
        """Intentar consultar actividades con caracteres especiales en las fechas"""
        with pytest.raises(FechaInvalidaError):
            self.actividad.consultar_actividades("@#$$%", "2025-03-06")

class TestGenerarReporte:
    
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.db.clear_tables()
        self.actividad = Actividad(self.db)
        self.bitacora = Bitacora(self.db)
    
    # ---- PRUEBAS NORMALES ----
    def test_generar_reporte_rango_valido(self):
        """Generar un reporte en un rango de fechas válido"""
        resultado = self.bitacora.generar_reporte("2025-03-01", "2025-03-10", "reporte.pdf")
        assert resultado is True
    
    def test_generar_reporte_sin_resultados(self):
        """Generar un reporte en un rango sin actividades registradas"""
        resultado = self.bitacora.generar_reporte("2030-01-01", "2030-01-10", "reporte_vacio.pdf")
        assert resultado is True  # El PDF debe generarse aunque esté vacío
    
    def test_generar_reporte_fecha_actual(self):
        """Generar un reporte con la fecha actual"""
        resultado = self.bitacora.generar_reporte("2025-03-06", "2025-03-06", "reporte_hoy.pdf")
        assert resultado is True
    
    # ---- PRUEBAS EXTREMAS ----
    def test_generar_reporte_rango_extremadamente_amplio(self):
        """Generar un reporte con un rango de fechas muy grande"""
        resultado = self.bitacora.generar_reporte("2000-01-01", "2100-12-31", "reporte_extremo.pdf")
        assert resultado is True
    
    def test_generar_reporte_mismo_dia(self):
        """Generar un reporte con las actividades de un solo día"""
        resultado = self.bitacora.generar_reporte("2025-03-06", "2025-03-06", "reporte_dia.pdf")
        assert resultado is True
    
    def test_generar_reporte_caracteres_especiales(self):
        """Generar un reporte con caracteres especiales en el nombre del archivo"""
        with pytest.raises(ReporteError):
            self.bitacora.generar_reporte("2025-03-06", "2025-03-06", "reporte_@#$%.pdf")

    
    # ---- PRUEBAS DE ERROR ----
    def test_generar_reporte_rango_invalido(self):
        """Generar un reporte con un rango de fechas inválido"""
        with pytest.raises(RangoFechasInvalidoError):
            self.bitacora.generar_reporte("2025-03-10", "2025-03-01", "reporte_invalido.pdf")

    def test_generar_reporte_sin_actividades(self):
        """Generar un reporte sin actividades registradas"""
    
        resultado = self.bitacora.generar_reporte("2030-01-01", "2030-01-10", "reporte_error.pdf")
    
        assert resultado is True

    
    def test_generar_reporte_nombre_archivo_invalido(self):
        """Intentar generar un reporte con un nombre de archivo inválido"""
        with pytest.raises(ReporteError):
            self.bitacora.generar_reporte("2025-03-06", "2025-03-06", "invalido@#.pdf")

import pytest
from src.model.usuario import Usuario
from src.model.database import Database
from src.model.errores import (
    CorreoYaRegistradoError,
    CamposVaciosError,
    ContrasenaIncorrectaError,
    UsuarioNoEncontradoError
)

class TestCrearCuenta:
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.db.clear_tables()
        self.usuario = Usuario(self.db)

    # ---- PRUEBAS NORMALES ----
    def test_crear_cuenta_exitosa(self):
        """Crear una cuenta con datos válidos"""
        resultado = self.usuario.crear_cuenta("Juan", "juan@example.com", "password123")
        assert resultado is True

    def test_crear_cuenta_con_email_existe(self):
        """Intentar crear una cuenta con un correo que ya está registrado"""
        self.usuario.crear_cuenta("Juan", "juan@example.com", "password123")
        with pytest.raises(CorreoYaRegistradoError):
            self.usuario.crear_cuenta("Juan", "juan@example.com", "nuevapassword")

    def test_crear_cuenta_con_datos_validos(self):
        """Crear una cuenta con datos correctos"""
        resultado = self.usuario.crear_cuenta("María", "maria@example.com", "password456")
        assert resultado is True

    # ---- PRUEBAS EXTREMAS ----
    def test_crear_cuenta_email_largo(self):
        """Crear una cuenta con un correo muy largo"""
        correo_largo = "a" * 250 + "@example.com"
        resultado = self.usuario.crear_cuenta("UsuarioExtremo", correo_largo, "password123")
        assert resultado is True

    def test_crear_cuenta_password_largo(self):
        """Crear una cuenta con una contraseña muy larga"""
        password_largo = "a" * 100
        resultado = self.usuario.crear_cuenta("Largo", "usuario@example.com", password_largo)
        assert resultado is True

    def test_crear_cuenta_con_formato_email_invalido(self):
        """Intentar crear una cuenta con un correo con formato inválido"""
        with pytest.raises(CamposVaciosError):
            self.usuario.crear_cuenta("Usuario", "usuario@invalido", "password123")

    # ---- PRUEBAS DE ERROR ----
    def test_crear_cuenta_con_campos_vacios(self):
        """Intentar crear una cuenta con campos vacíos"""
        with pytest.raises(CamposVaciosError):
            self.usuario.crear_cuenta("", "", "")

    def test_crear_cuenta_con_email_mal_formado(self):
        """Intentar crear una cuenta con email sin dominio"""
        with pytest.raises(CamposVaciosError):
            self.usuario.crear_cuenta("Usuario", "invalido@com", "password")

    def test_crear_cuenta_con_contrasena_corta(self):
        """Intentar crear una cuenta con una contraseña muy corta"""
        with pytest.raises(CamposVaciosError):
            self.usuario.crear_cuenta("Usuario", "invalido@example.com", "123")



class TestIniciarSesion:
    
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.db.clear_tables()
        self.usuario = Usuario(self.db)

    # ---- PRUEBAS NORMALES ----
    def test_iniciar_sesion_exitosa(self):
        """Iniciar sesión con credenciales válidas"""
        self.usuario.crear_cuenta("Juan", "juan@example.com", "password123")
        resultado = self.usuario.iniciar_sesion("juan@example.com", "password123")
        assert resultado is not None  # Devuelve tupla (id, nombre, correo, contrasena)
        assert resultado[1] == "Juan"
        assert resultado[2] == "juan@example.com"

    def test_iniciar_sesion_contrasena_incorrecta(self):
        """Intentar iniciar sesión con la contraseña incorrecta"""
        self.usuario.crear_cuenta("Juan", "juan@example.com", "password123")
        with pytest.raises(ContrasenaIncorrectaError):
            self.usuario.iniciar_sesion("juan@example.com", "wrongpassword")

    def test_iniciar_sesion_usuario_inexistente(self):
        """Intentar iniciar sesión con un correo que no existe"""
        with pytest.raises(UsuarioNoEncontradoError):
            self.usuario.iniciar_sesion("noexiste@example.com", "password123")

    # ---- PRUEBAS EXTREMAS ----
    def test_iniciar_sesion_email_largo(self):
        """Intentar iniciar sesión con un correo muy largo"""
        correo_largo = "a" * 250 + "@example.com"
        self.usuario.crear_cuenta("UsuarioLargo", correo_largo, "password123")
        resultado = self.usuario.iniciar_sesion(correo_largo, "password123")
        assert resultado[2] == correo_largo

    def test_iniciar_sesion_contrasena_larga(self):
        """Iniciar sesión con una contraseña muy larga"""
        password_largo = "a" * 100
        self.usuario.crear_cuenta("Usuario", "usuario@example.com", password_largo)
        resultado = self.usuario.iniciar_sesion("usuario@example.com", password_largo)
        assert resultado[3] == password_largo

    def test_iniciar_sesion_contrasena_vacia(self):
        """Intentar iniciar sesión con la contraseña vacía"""
        self.usuario.crear_cuenta("Juan", "juan@example.com", "correcta123")
        with pytest.raises(CamposVaciosError):
            self.usuario.iniciar_sesion("juan@example.com", "")

    # ---- PRUEBAS DE ERROR ----
    def test_iniciar_sesion_usuario_inexistente_error(self):
        """Intentar iniciar sesión con un usuario que no existe"""
        with pytest.raises(UsuarioNoEncontradoError):
            self.usuario.iniciar_sesion("desconocido@example.com", "ClaveInvalida")

    def test_iniciar_sesion_contrasena_incorrecta_error(self):
        """Intentar iniciar sesión con una contraseña incorrecta"""
        self.usuario.crear_cuenta("Juan", "juan@example.com", "correcta123")
        with pytest.raises(ContrasenaIncorrectaError):
            self.usuario.iniciar_sesion("juan@example.com", "ClaveIncorrecta")

    def test_iniciar_sesion_sin_parametros(self):
        """Intentar iniciar sesión sin ingresar usuario ni contraseña"""
        with pytest.raises(CamposVaciosError):
            self.usuario.iniciar_sesion("", "")

class TestCambiarContrasena:
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()

        self.db.clear_tables()

        self.usuario = Usuario(self.db)
        self.usuario.crear_cuenta("Juan Pérez", "juan@example.com", "Password123")
    
    # ---- PRUEBAS NORMALES ----
    def test_cambiar_contrasena_valida(self):
        """Cambiar contraseña con credenciales correctas"""
        resultado = self.usuario.cambiar_contrasena("juan@example.com", "NuevaPassword456")
        assert resultado is True
    
    def test_cambiar_contrasena_varias_veces(self):
        """Cambiar contraseña dos veces seguidas"""
        self.usuario.cambiar_contrasena("juan@example.com", "NuevaClave1")
        resultado = self.usuario.cambiar_contrasena("juan@example.com", "NuevaClave2")
        assert resultado is True
    
    def test_cambiar_contrasena_despues_de_creacion(self):
        """Cambiar contraseña inmediatamente después de crear una cuenta"""
        self.usuario.crear_cuenta("María López", "maria@example.com", "ClaveSegura123")
        resultado = self.usuario.cambiar_contrasena("maria@example.com", "NuevaClave789")
        assert resultado is True
    
    # ---- PRUEBAS EXTREMAS ----
    def test_cambiar_contrasena_muy_larga(self):
        """Cambiar contraseña con una contraseña extremadamente larga"""
        contrasena_larga = "A" * 100
        resultado = self.usuario.cambiar_contrasena("juan@example.com", contrasena_larga)
        assert resultado is True
    
    def test_cambiar_contrasena_con_caracteres_especiales(self):
        """Cambiar contraseña con caracteres especiales"""
        resultado = self.usuario.cambiar_contrasena("juan@example.com", "Clave$%&/()=?")
        assert resultado is True
    
    def test_cambiar_contrasena_a_misma_clave(self):
        """Intentar cambiar la contraseña a la misma que ya tenía"""
        with pytest.raises(ValueError):
            self.usuario.cambiar_contrasena("juan@example.com", "Password123")
    
    # ---- PRUEBAS DE ERROR ----
    def test_cambiar_contrasena_usuario_inexistente(self):
        """Intentar cambiar la contraseña de un usuario que no existe"""
        with pytest.raises(UsuarioNoEncontradoError):
            self.usuario.cambiar_contrasena("desconocido@example.com", "NuevaClave")
    
    def test_cambiar_contrasena_sin_parametros(self):
        """Intentar cambiar la contraseña sin proporcionar parámetros"""
        with pytest.raises(CamposVaciosError):
            self.usuario.cambiar_contrasena("", "")
    
    def test_cambiar_contrasena_sin_contrasena_nueva(self):
        """Intentar cambiar la contraseña sin proporcionar la nueva contraseña"""
        with pytest.raises(CamposVaciosError):
            self.usuario.cambiar_contrasena("juan@example.com", "")