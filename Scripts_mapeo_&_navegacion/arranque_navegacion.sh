#!/bin/bash
# ====================================================================
# VARIABLES DE ENTORNO Y OPTIMIZACIONES GRÁFICAS PARA INTEL
# ====================================================================
export LIBGL_ALWAYS_SOFTWARE=0
export OGRE_RTT_MODE=Copy            # Evita el crash de texturas de mapa en RViz2
#export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp  # <-- Dejar inhabilitado por ahora 
export ROS_LOCALHOST_ONLY=1
export msaa=0                        # Quita antialiasing para no congelar RViz2

echo "=== Arrancando Sistema Robotizado Centralizado ==="

# Deshabilitar autosuspend USB (Kinect y Kobuki estables sin caídas de energía)
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
sleep 2

# Terminal 1- Filtro Laserscan
gnome-terminal --tab --title="1. Filtro" -- bash -c "source ~/.bashrc && ros2 run kobuki_trajectories filtro_laserscan; exec bash" &
sleep 5

# --------------------------------------------------------------------
# Terminal - El Cerebro Completo (Tu slam.launch.py)
# --------------------------------------------------------------------
# Esto ejecutará de forma ordenada: Kobuki, Kinect, Laserscan, EKF, SLAM y RViz2 sin duplicados.
gnome-terminal --tab --title="2. Lanzamiento Maestro ROS 2" -- bash -c "source ~/.bashrc && ros2 launch kobuki_launch navegacion.launch.py; exec bash" &

