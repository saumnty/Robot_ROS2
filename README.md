# Diseño y Validación de Estrategia de Control Adaptativo/Inteligente para Robots Móviles mediante co-simulación (ROS2, Gazebo y MATLAB/Simulink) 

Este repositorio contiene la arquitectura de simulación en lazo cerrado (Full-Duplex) para el robot **Bolitabot**. Permite controlar al robot en un entorno virtual 3D mientras se calculan sus trayectorias matemáticas en tiempo real.

## Arquitectura del Sistema

El proyecto conecta **MATLAB/Simulink** (cerebro matemático) con **Gazebo Harmonic / ROS 2** (motor físico) a través de una red TCP/IP y un nodo puente (Bridge) en Python.
El robot sigue trayectorias generadas mediante **Splines Cúbicos de Hermite**, utilizando un controlador de punto adelantado (*Look-ahead point*).

## Requisitos Previos e Instalación

Para ejecutar este proyecto sin problemas, necesitas tener instaladas las siguientes herramientas:

1. **Sistema Operativo:** Ubuntu 22.04 / 24.04 (Nativo o vía WSL2 en Windows).
2. **Docker:** Motor de Docker instalado y configurado.
3. **MATLAB / Simulink:** Versión R2023a o superior (Se requiere soporte para funciones de TCP/IP e integración con Python).
4. **Python:** Python 3.10+ (Para el motor de Hermite dentro de MATLAB).

> **Nota sobre Docker:** Toda la instalación de ROS 2 (Jazzy) y Gazebo ya está empaquetada o se autoconfigura en el contenedor. No necesitas instalar ROS nativamente en tu PC.

## Cómo Ejecutar la Simulación

**1. Lanzar el entorno (Servidor y Motor Físico)**
El script principal de Docker está configurado para permitirte elegir el entorno de simulación. En la raíz de este repositorio, asegúrate de darle permisos de ejecución al script:

```bash
chmod +x pt_run.sh
```

A continuación, lanza el script. Tienes dos opciones de mundo:

* **Opción A: Mundo Vacío (Plano de pruebas)** Es el entorno por defecto (`bolitabot_void.sdf`). Ideal para depurar trayectorias matemáticas puras (como el trébol) sin obstáculos.

```bash
./pt_run.sh
# o explícitamente:
./pt_run.sh vacio
```

* **Opción B: Cuarto Piso** Carga el mundo arquitectónico completo (`bolitabot_world.sdf`). Ideal para probar el desempeño en un entorno real.

```bash
./pt_run.sh cuarto
```

> **Tip de Velocidad:** Si notas que el script tarda varios segundos descargando paquetes (`apt`), puedes hacer que el arranque sea casi instantáneo siguiendo las instrucciones en [⚡ Optimización del Inicio (Docker)](#-optimización-del-inicio-docker) al final de este documento.

**2. Iniciar el Cerebro (MATLAB)**

1. Abre MATLAB y usa el explorador de archivos izquierdo ("Current Folder") para navegar hasta la carpeta `bolitabot`.
2. Da clic derecho sobre la carpeta `bolitabot`, selecciona **"Add to Path"** y luego haz clic en **"Selected Folders and Subfolders"**. Esto es crucial para que MATLAB detecte todas las funciones.
3. Abre el modelo de Simulink (`controlador_trebol.slx` o equivalente).
4. Asegúrate de que la terminal de Docker ya imprimió `"--> Abriendo canal Full-Duplex para MATLAB..."`.
5. ¡Dale a **Run** en Simulink! *(Si obtienes un error relacionado con Python, consulta la sección de [Solución de problemas comunes](#-solución-de-problemas-comunes)).*

---

## Estructura del Repositorio

* `pt_run.sh`: Script principal de automatización de Docker con selector de mundos y configuración de entorno.
* `meshes/`: Carpeta con los modelos 3D (colladas/STLs), texturas e imágenes necesarias para renderizar el escenario arquitectónico (cuarto piso) en Gazebo.
* `bolitabot/`: Directorio principal del proyecto que contiene los modelos, mundos y la lógica de control.
* `bolitabot_void.sdf`: Entorno de pruebas plano y sin obstáculos (Mundo Vacío).
* `bolitabot_world.sdf`: Entorno de simulación realista que representa el Cuarto Piso.
* `bolitabot_casters.sdf`: Modelo físico y cinemático del robot Bolitabot (contiene su geometría, colisiones y el plugin de tracción diferencial).
* `servidor_cmd.py`: Nodo de ROS 2 que implementa el servidor TCP Full-Duplex. Se encarga de recibir las velocidades desde MATLAB, publicarlas en Gazebo y devolver la odometría en tiempo real.
* `brain_hermite.py`: Motor matemático en Python (invocado por MATLAB) que calcula instantáneamente la posición y velocidad usando Splines Cúbicos de Hermite.
* `get_tramo.m`: Función de MATLAB con la lógica geométrica y las condiciones de frontera (vectores tangentes) para trazar la pista deseada.
* `sfunc_bolitabot.m`: Bloque S-Function de Simulink que gestiona el socket TCP bidireccional y previene cuelgues durante la simulación.
* `controlador_trebol.slx`: Modelo principal de Simulink. Contiene el lazo de control cerrado, el cálculo del punto adelantado (*look-ahead point*) y la gráfica XY de odometría.

---

## Solución de problemas comunes

**Error de Python en MATLAB**
Si al darle a *Run* en Simulink, la simulación se detiene y la *Command Window* de MATLAB muestra el siguiente error:

```matlab
Error:Undefined function 'py.brain_hermite.get_hermite_point' for input arguments of type 'cell'.
    Error in 'controlador_trebol/MATLAB Function' (line 47)
        res_py = py.brain_hermite.get_hermite_point( ...
```

**¿Por qué pasa?** MATLAB no sabe dónde buscar los archivos de Python (`brain_hermite.py`), incluso si ya agregaste la carpeta al Path normal.

**Solución:** Copia y pega el siguiente código directamente en la Command Window (la consola de comandos) de MATLAB y presiona Enter. Esto agregará la ruta al motor interno de Python. (*Nota: Si prefieres, puedes cambiar `pwd` por tu ruta absoluta, ej: `'/home/usuario/mis_robots/bolitabot'*`):

```matlab
miRuta = pwd; 
if count(py.sys.path, miRuta) == 0
    insert(py.sys.path, int32(0), miRuta);
end
```

Una vez ejecutado, vuelve a darle a Run en Simulink y funcionará perfectamente.

---

## Optimización del Inicio (Docker)

Debido a que el script destruye el contenedor en cada reinicio para evitar conflictos, la imagen base vuelve a descargar e instalar Gazebo vía `apt` cada vez que se ejecuta. Para congelar esta instalación y reducir el tiempo de carga a **solo 3 segundos**, realiza este procedimiento por única vez:

1. Ejecuta el entorno normalmente una vez con `./pt_run.sh`.
2. Mientras la simulación esté corriendo (y ya haya terminado de instalar Gazebo), abre **una nueva terminal** en tu computadora y ejecuta:

   ```bash
   docker commit robot osrf/ros:jazzy-desktop-gz
   ```

   *(Esto empaquetará el contenedor actual en una nueva imagen local. Puede tardar un par de minutos).*
3. Abre el archivo `pt_run.sh` con tu editor de texto y busca la línea que define la imagen de Docker (alrededor de la línea 35):

   ```bash
   # Cambia esto:
   osrf/ros:jazzy-desktop \

   # Por esto:
   osrf/ros:jazzy-desktop-gz \
   ```

A partir de ahora, tu script arrancará usando la imagen con Gazebo preinstalado y saltará automáticamente el paso de descargas.
