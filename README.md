# Proyecto Bolitabot 🤖🚗

Este repositorio contiene la arquitectura de simulación en lazo cerrado (Full-Duplex) para el robot **Bolitabot**. Permite controlar al robot en un entorno virtual 3D mientras se calculan sus trayectorias matemáticas en tiempo real.

## 🌟 Arquitectura del Sistema
El proyecto conecta **MATLAB/Simulink** (cerebro matemático) con **Gazebo Harmonic / ROS 2** (motor físico) a través de una red TCP/IP y un nodo puente (Bridge) en Python. 
El robot sigue trayectorias generadas mediante **Splines Cúbicos de Hermite**, utilizando un controlador de punto adelantado (*Look-ahead point*).

## 🛠️ Requisitos Previos e Instalación

Para ejecutar este proyecto sin problemas, necesitas tener instaladas las siguientes herramientas:

1. **Sistema Operativo:** Ubuntu 22.04 / 24.04 (Nativo o vía WSL2 en Windows).
2. **Docker:** Motor de Docker instalado y configurado.
3. **MATLAB / Simulink:** Versión R2023a o superior (Se requiere soporte para funciones de TCP/IP e integración con Python).
4. **Python:** Python 3.10+ (Para el motor de Hermite dentro de MATLAB).

> **Nota sobre Docker:** Toda la instalación de ROS 2 (Jazzy) y Gazebo ya está empaquetada o se autoconfigura en el contenedor. No necesitas instalar ROS nativamente en tu PC.

# 🚀 Cómo Ejecutar la Simulación

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
**2. Iniciar el Cerebro (MATLAB)**
 1. Abre MATLAB y navega hasta la carpeta `bolitabot`.
 2. Abre el modelo de Simulink (`controlador_trebol.slx` o equivalente).
 3. Asegúrate de que la terminal de Docker ya imprimió `"Servidor Full-Duplex listo..."`.
 4. ¡Dale a Run en Simulink!
    
## 📁 Estructura del Repositorio
* `pt_run.sh`: Script principal de automatización de Docker con selector de mundos.
* `bolitabot/`: Carpeta con los modelos SDF del robot, mundos de Gazebo y scripts de Python/MATLAB.
  * `bolitabot_void.sdf`: Entorno de pruebas plano.
  * `bolitabot_world.sdf`: Entorno de pruebas del cuarto piso.
  * `servidor_cmd.py`: Nodo de ROS 2 que expone el socket TCP bidireccional.
  * `brain_hermite.py`: Generador matemático de trayectorias.
  * `get_tramo.m`: Lógica de control para la generación de la pista.
  * `sfunc_bolitabot.m`: S-Function de Simulink para enviar velocidades y recibir odometría.
