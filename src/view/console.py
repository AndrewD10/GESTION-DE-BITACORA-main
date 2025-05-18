"""
Módulo de menú por consola para la aplicación de gestión de bitácoras.

Este menú permite al usuario interactuar con el sistema mediante opciones
como registrar actividades, generar reportes, autenticarse, etc.
"""

from src.model.actividad import Actividad
from src.model.bitacora import Bitacora
from src.model.usuario import Usuario
from src.model.errores import *
from src.model.sesion import guardar_sesion, obtener_sesion, cerrar_sesion
from src.model.database import Database

# Instancias de modelos
actividad_model = Actividad(Database)
bitacora_model = Bitacora(Database)
usuario_model = Usuario(Database)


def mostrar_menu():
    """Muestra el menú principal con el nombre del usuario activo si existe."""
    usuario = obtener_sesion()
    nombre = usuario["nombre"] if usuario else "ninguno"
    print(f"\n--- MENÚ PRINCIPAL --- (usuario activo: {nombre})")
    print("1. Registrar actividad")
    print("2. Consultar actividades")
    print("3. Generar reporte")
    print("4. Crear cuenta de usuario")
    print("5. Iniciar sesión")
    print("6. Cambiar contraseña")
    print("7. Cerrar sesión")
    print("0. Salir")


def registrar_actividad():
    """Registra una nueva actividad. Requiere sesión activa."""
    usuario = obtener_sesion()
    if not usuario:
        print("Error: Debes iniciar sesión primero.")
        return

    datos = {
        "fecha": input("Fecha (YYYY-MM-DD): "),
        "supervisor": input("Supervisor: "),
        "descripcion": input("Descripción: "),
        "anexos": input("Anexos: "),
        "responsable": input("Responsable: "),
        "clima": input("Clima: ")
    }

    try:
        actividad_model.registrar_actividad(datos)
        print("Actividad registrada exitosamente.")
    except BaseError as e:
        print(f"Error: {str(e)}")


def consultar_actividades():
    """Consulta actividades entre dos fechas. Requiere sesión activa."""
    if not obtener_sesion():
        print("Error: Debes iniciar sesión primero.")
        return

    fi = input("Fecha inicio (YYYY-MM-DD): ")
    ff = input("Fecha fin (YYYY-MM-DD): ")

    try:
        actividades = actividad_model.consultar_actividades(fi, ff)
        if actividades:
            print("\nActividades encontradas:")
            for a in actividades:
                print(a)
        else:
            print("No se encontraron actividades.")
    except BaseError as e:
        print(f"Error: {str(e)}")


def generar_reporte():
    """Genera un reporte PDF. Requiere sesión activa."""
    if not obtener_sesion():
        print("Error: Debes iniciar sesión primero.")
        return

    fi = input("Fecha inicio (YYYY-MM-DD): ")
    ff = input("Fecha fin (YYYY-MM-DD): ")
    pdf = input("Nombre del archivo PDF (sin extensión): ")

    try:
        if bitacora_model.generar_reporte(fi, ff, pdf):
            print("Reporte generado exitosamente.")
        else:
            print("No hay actividades en ese rango de fechas.")
    except BaseError as e:
        print(f"Error: {str(e)}")


def crear_cuenta():
    """Crea una nueva cuenta de usuario y la inicia automáticamente."""
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    try:
        usuario_model.crear_cuenta(nombre, correo, contrasena)
        guardar_sesion({"correo": correo, "nombre": nombre})
        print("Cuenta creada e iniciada sesión exitosamente.")
    except BaseError as e:
        print(f"Error: {str(e)}")


def iniciar_sesion():
    """Permite a un usuario iniciar sesión."""
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    try:
        user = usuario_model.iniciar_sesion(correo, contrasena)
        guardar_sesion({"correo": correo, "nombre": user['nombre']})
        print(f"Bienvenido {user['nombre']}")
    except BaseError as e:
        print(f"Error: {str(e)}")


def cambiar_contrasena():
    """Permite cambiar la contraseña del usuario autenticado. Cierra sesión por seguridad."""
    usuario = obtener_sesion()
    if not usuario:
        print("Error: Debes iniciar sesión primero.")
        return

    nueva_contrasena = input("Nueva contraseña: ")

    try:
        usuario_model.cambiar_contrasena(usuario["correo"], nueva_contrasena)
        cerrar_sesion()
        print("Contraseña cambiada. Se cerró la sesión por seguridad.")
    except BaseError as e:
        print(f"Error: {str(e)}")


def cerrar_sesion_consola():
    """Cierra la sesión activa."""
    if obtener_sesion():
        cerrar_sesion()
        print("Sesión cerrada.")
    else:
        print("No hay sesión activa.")


def main():
    """Ejecuta el menú principal."""
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_actividad()
        elif opcion == "2":
            consultar_actividades()
        elif opcion == "3":
            generar_reporte()
        elif opcion == "4":
            crear_cuenta()
        elif opcion == "5":
            iniciar_sesion()
        elif opcion == "6":
            cambiar_contrasena()
        elif opcion == "7":
            cerrar_sesion_consola()
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
