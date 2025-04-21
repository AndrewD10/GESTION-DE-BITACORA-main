import json
import os

RUTA_SESION = "sesion.json"

def guardar_sesion(usuario: dict):
    with open(RUTA_SESION, "w") as f:
        json.dump(usuario, f)

def obtener_sesion():
    if not os.path.exists(RUTA_SESION):
        return None
    try:
        with open(RUTA_SESION, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None

def cerrar_sesion():
    if os.path.exists(RUTA_SESION):
        os.remove(RUTA_SESION)
