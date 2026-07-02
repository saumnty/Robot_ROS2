#!/bin/bash

# 1. Leer el argumento del mundo (vacío por defecto si no escribes nada)
MUNDO=${1:-vacio}

if [ "$MUNDO" = "cuarto" ]; then
    MUNDO_SDF="bolitabot_world.sdf" 
    TEXTO_MUNDO="Cuarto Piso"
else
    MUNDO_SDF="bolitabot_void.sdf"
    TEXTO_MUNDO="Vacío (Plano)"
fi

echo "================================================="
echo " Iniciando entorno Bolitabot "
echo " Mundo seleccionado: $TEXTO_MUNDO"
echo "================================================="

# 2. Permisos de pantalla y limpieza rápida
xhost +local:docker > /dev/null
docker rm -f robot 2>/dev/null

# 3. Iniciar el contenedor con variables nativas
docker run -d \
  --name robot \
  --privileged \
  --network host \
  --ipc host \
  -e DISPLAY=$DISPLAY \
  -e GZ_SIM_RESOURCE_PATH=/root/mis_robots/bolitabot:/root/mis_robots/bolitabot/meshes \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/$USER/mis_robots/bolitabot:/root/mis_robots/bolitabot \
  --device /dev/dri:/dev/dri \
  osrf/ros:jazzy-desktop \
  sleep infinity

# 4. Ejecución Unificada dentro de Docker
docker exec -it robot bash -c "
  # El echo condicional que pediste (solo se imprime si entra al IF)
  if ! command -v gz &> /dev/null; then 
    echo '--> [AVISO] Primera ejecución detectada. Instalando ros-jazzy-ros-gz...'
    echo '--> Esto puede tardar unos segundos...'
    apt update && apt install -y ros-jazzy-ros-gz > /dev/null
    echo '--> [OK] Instalación de Gazebo completada.'
  fi
  
  # Cargar ROS 2
  source /opt/ros/jazzy/setup.bash
  
  echo '--> Lanzando Gazebo con $MUNDO_SDF...'
  gz sim -r /root/mis_robots/bolitabot/$MUNDO_SDF &
  
  sleep 3 
  
  echo '--> Conectando Bridge ROS-Gazebo...'
  ros2 run ros_gz_bridge parameter_bridge \
    /model/bolitabot/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist \
    /model/bolitabot/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry &
    
  echo '--> Abriendo canal Full-Duplex para MATLAB...'
  python3 /root/mis_robots/bolitabot/servidor_cmd.py
"
