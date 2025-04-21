# Gestión de bitácora
El objetivo de este proyecto es garantizar la trazabilidad de las actividades 
realizadas en la obra.  Las funcionalidades que la aplicación debe tener son: 

1. Registrar una actividad: El sistema debe permitir a los supervisores registrar una actividad 
hecha en un día y una hora especifica.  
2. Consultar actividades: El sistema debe permitir a los supervisores consultar las actividades 
hechas en un rango de fechas en específico. 
3. Generar reporte de la bitácora: El sistema debe permitir a los supervisores generar un 
reporte en PDF sobre las actividades hechas en un rango de fechas en específico 
4. Crear cuenta: Los supervisores deben poder darse de alta en el sistema 
5. Iniciar sesión: Los supervisores deben poder iniciar sesión en la aplicación 
6. Cambiar contraseña: Los supervisores debe poder cambiar su contraseña cuando lo 
deseen.  

Una actividad debe estar compuesta por los siguientes datos: 

1. Fecha y hora de la actividad 
2. Supervisor que creó la actividad 
3. Texto que describe la actividad 
4. Anexos (Imágenes o documentos) 
5.  Responsable de esa actividad (Quien la realizó) 
6. Condiciones climáticas durante la actividad

**Nota**: Cada supervisor al crear su cuenta e iniciar sesión debe poder ver todas las actividades 
registradas en el sistema, sin importar si otros supervisores crearon la actividad.

## Diagrama de Clases

![alt text](<assets/Clase UML.png>)

## Implementacion de las pruebas

### **Registrar actividad**

Pruebas Normales

| #  | Descripción                               | Datos de entrada                           | Resultado esperado    |
|----|-----------------------------------------  |------------------------------------------- |--------------------   |
| 1  | Registrar una actividad con datos válidos | Fecha: "2025-03-06", Supervisor: "Juan",   | Actividad registrada  |
|                                                   Descripción: "Revisión", Clima: "Soleado"  |
| 2  | Registrar una actividad sin anexo         | Fecha: "2025-03-06", Supervisor: "Juan",   | Actividad registrada  |
|                                                  "Limpieza", Clima: "Nublado"                |

|                                                 |  Descripción: "Revisión", Clima: "Soleado" |                      |
| 2  | Registrar una actividad sin anexo         | Fecha: "2025-03-06", Supervisor: "Juan",   | Actividad registrada  |
|                                                |  "Limpieza", Clima: "Nublado"              |                       |

| 3  | Registrar una actividad con clima variable| Fecha: "2025-03-06", Supervisor: "Juan",   | Actividad registrada  |
                                                  "Reparación", Clima: "Lluvia intermitente"

Pruebas Extremas

| #  | Descripción                                   | Datos de entrada                           | Resultado esperado   |
|----|--------------------------------------------- |------------------------------------------- |--------------------   |
| 4  | Registrar actividad con fecha muy lejana     | Fecha: "2035-12-31", Supervisor: "Juan"    | Actividad registrada  |
| 5  | Registrar actividad con descripción muy larga| Descripción: 1000 caracteres               | Actividad registrada  |
| 6  | Registrar actividad con clima poco común     | Clima: "Huracán categoría 5"               | Actividad registrada  |

Pruebas de Error

| #  | Descripción                                    | Datos de entrada                           | Resultado esperado    |
|----|---------------------------------------------- |------------------------------------------- |--------------------   |
| 7  | Intentar registrar actividad con fecha inválida  | Fecha: "fecha_invalida"                 | Lanza `FechaInvalidaError` |
| 8  | Intentar registrar actividad sin descripción  | Descripción: ""                           | Lanza `CamposVaciosError`  |
| 9  | Intentar registrar actividad sin responsable  | Responsable: ""                           | Lanza `CamposVaciosError`  |

### **Consultar actividades**

Pruebas Normales

| #  | Descripción                                     | Datos de entrada                               | Resultado esperado    |
|----|----------------------------------------------  |----------------------------------------------- |--------------------   |
| 1  | Consultar actividades dentro de un rango válido | Fecha inicio: "2025-03-01", Fecha fin: "2025-03-10" | Devuelve lista de 

|                                                                                                              actividades|

|                                                      |                                                       actividades|

| 2  | Consultar actividades sin resultados          | Fecha inicio: "2030-01-01", Fecha fin: "2030-01-10" | Devuelve lista vacía |
| 3  | Consultar actividades en la fecha actual      | Fecha: "2025-03-06"                          | Devuelve lista de actividades |

Pruebas Extremas

| #  | Descripción                                | Datos de entrada                               | Resultado esperado    |
|----|------------------------------------------  |----------------------------------------------- |--------------------   |
| 4  | Consultar actividades con rango muy amplio | Fecha inicio: "2000-01-01", Fecha fin: "2100-12-31" | Devuelve lista de 

|                                                                                                          actividades |

|                                                 |                                                         actividades |

| 5  | Consultar actividades en un solo día      | Fecha inicio: "2025-03-06", Fecha fin: "2025-03-06" | Devuelve lista de actividades |
| 6  | Consultar actividades con fechas invertidas | Fecha inicio: "2025-03-10", Fecha fin: "2025-03-01" | Devuelve lista vacía |

Pruebas de Error

| #  | Descripción                                  | Datos de entrada                  | Resultado esperado        |
|----|-------------------------------------------- |--------------------------------- |-------------------------- |
| 7  | Consultar actividades con fechas inválidas | Fecha inicio: "fecha_invalida"   | Lanza `FechaInvalidaError` |
| 8  | Consultar actividades sin fechas           | Fecha inicio: "", Fecha fin: ""  | Lanza `CamposVaciosError` |
| 9  | Consultar actividades con caracteres inválidos | Fecha inicio: "@#$$%"         | Lanza `FechaInvalidaError` |


### **Generar reporte**

Pruebas Normales

| #  | Descripción                               | Datos de entrada                                     | Resultado esperado     |
|----|-----------------------------------------  |-----------------------------------------------       |--------------------    |
| 1  | Generar un reporte en un rango válido     | Fecha inicio: "2025-03-01", Fecha fin: "2025-03-10", | Reporte generado

|                                                  Archivo: "reporte.pdf"                                                         |
| 2  | Generar un reporte sin actividades       | Fecha inicio: "2030-01-01", Fecha fin: "2030-01-10",  | Reporte generado       |
|                                                 Archivo: "reporte_vacio.pdf" 

|                                                |  Archivo: "reporte.pdf"                              |                           |
| 2  | Generar un reporte sin actividades       | Fecha inicio: "2030-01-01", Fecha fin: "2030-01-10",  | Reporte generado       |
|                                               |   Archivo: "reporte_vacio.pdf"                        |                         |

| 3  | Generar un reporte con la fecha actual  | Fecha: "2025-03-06", Archivo: "reporte_hoy.pdf"        | Reporte generado       | 

Pruebas Extremas

| #  | Descripción                                      | Datos de entrada                                | Resultado esperado        |
|----|-----------------------------------------------  |-----------------------------------------------  |--------------------        |
| 4  | Generar un reporte en un rango muy amplio     | Fecha inicio: "2000-01-01", Fecha fin: "2100-12-31" | Reporte generado         |
| 5  | Generar un reporte con un solo día de rango   | Fecha inicio: "2025-03-06", Fecha fin: "2025-03-06" | Reporte generado         |
| 6  | Generar un reporte con fechas invertidas      | Fecha inicio: "2025-03-10", Fecha fin: "2025-03-01" | Lanza 
 |                                                                                                          `RangoFechasInvalidoError` |

Pruebas de Error

| #  | Descripción                                      | Datos de entrada                       | Resultado esperado         |
|----|-----------------------------------------------  |--------------------------------------- |--------------------------  |
| 7  | Generar un reporte con fechas inválidas       | Fecha inicio: "fecha_invalida"         | Lanza `FechaInvalidaError` |
| 8  | Generar un reporte sin proporcionar fechas    | Fecha inicio: "", Fecha fin: ""       | Lanza `CamposVaciosError` |
| 9  | Generar un reporte con nombre de archivo inválido | Archivo: ""                       | Lanza `ReporteError` |

### **Crear cuenta**

Pruebas Normales

| #  | Descripción                              | Datos de entrada                                    | Resultado esperado  |
|----|----------------------------------------- |--------------------------------------------------- |-------------------- |
| 1  | Crear una cuenta con datos válidos      | Nombre: "Juan Pérez", Correo: "juan@example.com",   | Cuenta creada      |
|    |                                         | Contraseña: "Password123"                          |                    |
| 2  | Crear múltiples cuentas con diferentes usuarios | Nombre: "María López", "Carlos Gómez"      | Cuentas creadas    |
| 3  | Crear una cuenta sin nombre             | Correo: "anonimo@example.com", Contraseña: "Clave123" | Cuenta creada      |

Pruebas Extremas

| #  | Descripción                                | Datos de entrada                                        | Resultado esperado  |
|----|------------------------------------------ |------------------------------------------------------ |-------------------- |
| 4  | Crear cuenta con nombre extremadamente largo | Nombre: "Juan" * 50, Correo: "juanlargo@example.com" | Cuenta creada      |
| 5  | Crear cuenta con contraseña muy larga    | Contraseña: "A" * 100                                 | Cuenta creada      |
| 6  | Crear cuenta con caracteres especiales   | Nombre: "Usuario#1!", Correo: "user!@example.com"    | Cuenta creada      |

Pruebas de Error


| #  | Descripción                                  | Datos de entrada                        | Resultado esperado          |
|----|-------------------------------------------- |---------------------------------------- |---------------------------- |
| 7  | Intentar crear cuenta sin correo          | Nombre: "Juan Pérez", Correo: ""       | Lanza `CamposVaciosError`  |
| 8  | Intentar crear cuenta sin contraseña      | Nombre: "Juan Pérez", Contraseña: ""   | Lanza `CamposVaciosError`  |
| 9  | Intentar crear cuenta con correo repetido | Correo: "juan@example.com" registrado  | Lanza `CorreoYaRegistradoError` |


### **Iniciar sesion**

Pruebas Normales

| #  | Descripción                                 | Datos de entrada                                       | Resultado esperado  |
|----|------------------------------------------- |------------------------------------------------------ |-------------------- |
| 1  | Iniciar sesión con credenciales correctas | Correo: "juan@example.com", Contraseña: "Password123"    | Inicio exitoso     |
| 2  | Iniciar sesión con otra cuenta válida     | Correo: "maria@example.com", Contraseña: "ClaveSegura123" | Inicio exitoso     |
| 3  | Iniciar sesión inmediatamente después de crear cuenta | Correo: "carlos@example.com", Contraseña: "OtraClave456" | Inicio 
|                                                                                                                         exitoso     |
                                                                                                                         
Pruebas Extremas

| #  | Descripción                                  | Datos de entrada                                    | Resultado esperado  |
|----|-------------------------------------------- |-------------------------------------------------- |-------------------- |
| 4  | Iniciar sesión con contraseña extremadamente larga | Contraseña: "A" * 100 | Inicio exitoso     |
| 5  | Iniciar sesión con caracteres especiales   | Correo: "user!@example.com", Contraseña: "Clave$123" | Inicio exitoso     |
| 6  | Iniciar sesión con un nombre de usuario muy largo | Nombre: "UsuarioLargo" * 20 | Inicio exitoso     |

Pruebas de Error

| #  | Descripción                                  | Datos de entrada                               | Resultado esperado              |
|----|-------------------------------------------- |---------------------------------------------- |-------------------------------- |
| 7  | Intentar iniciar sesión con usuario inexistente | Correo: "desconocido@example.com"           | Lanza          

|                                                                                                     `UsuarioNoEncontradoError` |
| 8  | Intentar iniciar sesión con contraseña incorrecta | Correo: "juan@example.com",    | Lanza 
                                                         Contraseña: "ClaveIncorrecta"    `ContrasenaIncorrectaError` |
| 9  | Intentar iniciar sesión sin ingresar usuario y contraseña | Correo: "", Contraseña: ""  | Lanza  
|                                                                                               `CamposVaciosError`  |

|                                                       |                                             `UsuarioNoEncontradoError` |
| 8  | Intentar iniciar sesión con contraseña incorrecta | Correo: "juan@example.com",    | Lanza                               |
|                                                        | Contraseña: "ClaveIncorrecta"  |  `ContrasenaIncorrectaError` |
| 9  | Intentar iniciar sesión sin ingresar usuario y contraseña | Correo: "", Contraseña: ""  | Lanza                  |
|                                                                 |                             | `CamposVaciosError`  |

### **Cambiar contraseña**

Pruebas Normales

| #  | Descripción                              | Datos de entrada                                      | Resultado esperado  |
|----|---------------------------------------- |----------------------------------------------------- |-------------------- |
| 1  | Cambiar contraseña con credenciales correctas | Correo: "juan@example.com", Nueva contraseña: "NuevaPassword456" | Contraseña 

|                                                                                                                         cambiada |
| 2  | Cambiar contraseña dos veces seguidas   | Nueva contraseña: "NuevaClave1", luego "NuevaClave2" | Contraseña cambiada |
| 3  | Cambiar contraseña después de crear cuenta | Correo: "maria@example.com", Nueva contraseña: "NuevaClave789" | Contraseña 
|                                                                                                                   cambiada |

|                                                    |                                                                  |   cambiada |
| 2  | Cambiar contraseña dos veces seguidas   | Nueva contraseña: "NuevaClave1", luego "NuevaClave2" | Contraseña cambiada |
| 3  | Cambiar contraseña después de crear cuenta | Correo: "maria@example.com", Nueva contraseña: "NuevaClave789" | Contraseña 
|                                                  |                                                                  cambiada |


Pruebas Extremas

| #  | Descripción                              | Datos de entrada                                    | Resultado esperado  |
|----|---------------------------------------- |-------------------------------------------------- |-------------------- |
| 4  | Cambiar contraseña con una contraseña extremadamente larga | Contraseña: "A" * 100 | Contraseña cambiada |
| 5  | Cambiar contraseña con caracteres especiales | Contraseña: "Clave$%&/()=?" | Contraseña cambiada |
| 6  | Intentar cambiar la contraseña a la misma   | Contraseña anterior: "Password123", Nueva: "Password123" | Lanza 

|                                                                                                              `CamposVaciosError` |

|                                                  |                                                            `CamposVaciosError` |


Pruebas de Error


| #  | Descripción                                     | Datos de entrada                          | Resultado esperado               |
|----|---------------------------------------------- |----------------------------------------- |---------------------------------- |
| 7  | Intentar cambiar la contraseña de usuario inexistente | Correo: "desconocido@example.com"       | Lanza 

|                                                                                                       `UsuarioNoEncontradoError` |
| 8  | Intentar cambiar la contraseña sin proporcionar datos | Correo: "", Contraseña: ""             | Lanza `CamposVaciosError`  |
| 9  | Intentar cambiar la contraseña sin ingresar nueva contraseña | Correo: "juan@example.com", Contraseña: "" | Lanza 
|                                                                                                                 `CamposVaciosError`  |

|                                                            |                                           `UsuarioNoEncontradoError` |
| 8  | Intentar cambiar la contraseña sin proporcionar datos | Correo: "", Contraseña: ""             | Lanza `CamposVaciosError`  |
| 9  | Intentar cambiar la contraseña sin ingresar nueva contraseña | Correo: "juan@example.com", Contraseña: "" | Lanza 
|                                                                    |                                            `CamposVaciosError`  |

