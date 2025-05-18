import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from functools import partial

from src.model.database import Database
from src.model.actividad import Actividad
from src.model.bitacora import Bitacora
from src.model.usuario import Usuario
from src.model.errores import *
from src.model.sesion import guardar_sesion, obtener_sesion, cerrar_sesion

# Inicialización de lógica
import src.model.database as db
actividad_model = Actividad(db)
bitacora_model = Bitacora(db)
usuario_model = Usuario(db)  # <- Aquí sin pasar db


class MenuPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label_usuario = Label(text="", size_hint_y=None, height=30)
        self.layout.add_widget(self.label_usuario)

        self.btn_logout = Button(text="Cerrar sesión", size_hint_y=None, height=50, background_color=(1, 0.5, 0, 1))
        self.btn_logout.bind(on_press=self.logout)

        opciones = [
            ("Registrar actividad", "registro"),
            ("Consultar actividades", "consulta"),
            ("Generar reporte", "reporte"),
            ("Crear cuenta de usuario", "crear_cuenta"),
            ("Iniciar sesión", "login"),
            ("Cambiar contraseña", "cambiar_contrasena"),
        ]

        self.botones = []
        for texto, screen_name in opciones:
            btn = Button(text=texto, size_hint_y=None, height=50)
            btn.bind(on_press=partial(self.cambiar_pantalla, screen_name))
            self.botones.append(btn)
            self.layout.add_widget(btn)

        self.layout.add_widget(self.btn_logout)

        salir = Button(text="Salir", size_hint_y=None, height=50, background_color=(1, 0, 0, 1))
        salir.bind(on_press=lambda x: App.get_running_app().stop())
        self.layout.add_widget(salir)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        usuario = obtener_sesion()
        if usuario:
            self.label_usuario.text = f"Sesión activa: {usuario['nombre']}"
            self.btn_logout.disabled = False
        else:
            self.label_usuario.text = "No hay sesión activa"
            self.btn_logout.disabled = True

    def cambiar_pantalla(self, screen_name, instance):
        if screen_name in ["registro", "consulta", "reporte", "cambiar_contrasena"] and not obtener_sesion():
            self.mostrar_popup("Debes iniciar sesión primero.")
        else:
            self.manager.current = screen_name

    def logout(self, instance):
        cerrar_sesion()
        self.manager.current = 'menu'
        for screen in self.manager.screens:
            if isinstance(screen, FormularioBase):
                for input_widget in screen.inputs.values():
                    input_widget.text = ""

    def mostrar_popup(self, mensaje):
        popup = Popup(title='Advertencia',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


class FormularioBase(Screen):
    campos = []
    boton_texto = ""
    accion = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView()
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.inputs = {}
        for campo in self.campos:
            label = Label(text=campo, size_hint_y=None, height=30)
            input_text = TextInput(multiline=False, size_hint_y=None, height=40)
            self.inputs[campo] = input_text
            self.layout.add_widget(label)
            self.layout.add_widget(input_text)

        boton = Button(text=self.boton_texto, size_hint_y=None, height=50)
        boton.bind(on_press=self.ejecutar_accion)
        self.layout.add_widget(boton)

        self.resultado = Label(text="", markup=True, size_hint_y=None, height=60)
        self.layout.add_widget(self.resultado)

        volver = Button(text="Volver", size_hint_y=None, height=40)
        volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(volver)

        scroll.add_widget(self.layout)
        self.add_widget(scroll)

    def ejecutar_accion(self, instance):
        try:
            valores = [self.inputs[c].text for c in self.campos]
            mensaje = self.accion(*valores)
            self.resultado.text = f"[color=00ff00]{mensaje}[/color]"
        except BaseError as e:
            self.resultado.text = f"[color=ff0000]Error: {str(e)}[/color]"


class RegistroActividad(FormularioBase):
    campos = ["Fecha", "Supervisor", "Descripción", "Anexos", "Responsable", "Clima"]
    boton_texto = "Registrar"

    def accion(self, fecha, supervisor, descripcion, anexos, responsable, clima):
        if not obtener_sesion():
            raise CamposVaciosError("Debes iniciar sesión primero.")

        datos = {
            "fecha": fecha,
            "supervisor": supervisor,
            "descripcion": descripcion,
            "anexos": anexos,
            "responsable": responsable,
            "clima": clima
        }
        actividad_model.registrar_actividad(datos)

        # Limpia los campos después de registrar
        for input_widget in self.inputs.values():
            input_widget.text = ""

        return "Actividad registrada exitosamente."



class CrearCuenta(FormularioBase):
    campos = ["Nombre", "Correo", "Contraseña"]
    boton_texto = "Crear cuenta"

    def accion(self, nombre, correo, contrasena):
        usuario_model.crear_cuenta(nombre, correo, contrasena)
        guardar_sesion({"correo": correo, "nombre": nombre})
        return "Cuenta creada exitosamente."


class IniciarSesion(FormularioBase):
    campos = ["Correo", "Contraseña"]
    boton_texto = "Iniciar sesión"

    def accion(self, correo, contrasena):
        user = usuario_model.iniciar_sesion(correo, contrasena)
        guardar_sesion({"correo": correo, "nombre": user['nombre']})
        return f"Bienvenido {user['nombre']}"


class CambiarContrasena(FormularioBase):
    campos = ["Nueva contraseña"]
    boton_texto = "Cambiar contraseña"

    def accion(self, nueva_contrasena):
        usuario = obtener_sesion()
        if not usuario:
            raise CamposVaciosError("Debe iniciar sesión para cambiar la contraseña.")
        usuario_model.cambiar_contrasena(usuario["correo"], nueva_contrasena)
        cerrar_sesion()
        App.get_running_app().stop()
        return "Contraseña cambiada. Se cerró la sesión por seguridad."


class Reporte(FormularioBase):
    campos = ["Fecha inicio", "Fecha fin", "Nombre PDF"]
    boton_texto = "Generar reporte"

    def accion(self, fi, ff, pdf):
        if not obtener_sesion():
            raise CamposVaciosError("Debes iniciar sesión primero.")
        if bitacora_model.generar_reporte(fi, ff, pdf):
            return "Reporte generado exitosamente."
        return "No hay actividades en ese rango de fechas."


class ConsultarActividades(FormularioBase):
    campos = ["Fecha inicio", "Fecha fin"]
    boton_texto = "Consultar"

    def accion(self, fi, ff):
        if not obtener_sesion():
            raise CamposVaciosError("Debes iniciar sesión primero.")
        actividades = actividad_model.consultar_actividades(fi, ff)
        if actividades:
            return "\n".join(str(a) for a in actividades)
        return "No se encontraron actividades."


class BitacoraApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(name='menu'))
        sm.add_widget(RegistroActividad(name='registro'))
        sm.add_widget(ConsultarActividades(name='consulta'))
        sm.add_widget(Reporte(name='reporte'))
        sm.add_widget(CrearCuenta(name='crear_cuenta'))
        sm.add_widget(IniciarSesion(name='login'))
        sm.add_widget(CambiarContrasena(name='cambiar_contrasena'))
        return sm
