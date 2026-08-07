# Sistema de Navegación Autónoma en Interiores — Kobuki (TurtleBot2) + Kinect

Documentación técnica del sistema de navegación autónoma en interiores desarrollado durante una estadía profesional, usando un robot Kobuki (TurtleBot2) equipado con un sensor de profundidad Kinect Xbox 360, sobre ROS 2 Humble.

Este repositorio sirve como **guía/manual** para estudiantes o investigadores que deseen reproducir el sistema desde cero: desde la instalación del entorno hasta la navegación autónoma con SLAM.

---

## Descripción del proyecto

El proyecto implementa un pipeline completo de navegación autónoma en interiores, desarrollado en siete etapas:

1. **Familiarización con el Kobuki** — control básico y verificación de comunicación
2. **Control de desplazamiento básico** — trayectorias controladas (líneas, giros)
3. **Integración de sensores** — Kinect Xbox 360 + conversión a LiDAR virtual
4. **Procesamiento de señales** — filtrado de ruido en `/scan`
5. **Implementación de SLAM** — mapeo con `slam_toolbox`
6. **Navegación autónoma en interiores ** — Nav2 + AMCL + localización
7. **Validación y documentación** — pruebas en laboratorio y pasillo

## Hardware utilizado

| Componente | Detalle |
|---|---|
| Robot base | Kobuki (TurtleBot2) |
| Sensor de profundidad | Kinect Xbox 360 |
| Computadora de a bordo | Lenovo IdeaPad Slim 3 15IRH8 (Intel i7-13620H, Intel Iris Xe) |
| Alimentación del Kinect | Puerto de 12V 1.5A del Kobuki — ver [troubleshooting](docs/troubleshooting.md)) |

## Software utilizado

| Software | Versión |
|---|---|
| Sistema operativo | Ubuntu 22.04.5 LTS |
| Framework robótico | ROS 2 Humble |
| Middleware DDS | Cyclone DDS (`rmw_cyclonedds_cpp`) |
| SLAM | `slam_toolbox` |
| Navegación | `navigation2` (Nav2) |
| Localización | AMCL + `robot_localization` (EKF) |

---

## Estructura del repositorio

```
├── docs/                          # Guías paso a paso (seguir en orden)
│   ├── 01-hardware-setup.md
│   ├── 02-software-setup.md
│   ├── 03-kobuki-basics.md
│   ├── 04-kinect-integration.md
│   ├── 05-sensor-processing.md
│   ├── 06-slam.md
│   ├── 07-navigation.md
│   ├── troubleshooting.md         # Problemas reales y sus soluciones
│   └── images/
├── src/                            # Paquetes ROS 2 propios (código fuente)
│   ├── kobuki_launch/
│   └── kobuki_trajectories/
└── config/                         # Archivos de configuración centralizados
    ├── nav2_params.yaml
    ├── mapper_params_online_async.yaml
    ├── ekf_config.yaml
    └── laserscan_config.yaml
```

> **Nota:** este repositorio solo incluye los paquetes desarrollados durante la estadía (`kobuki_launch`, `kobuki_trajectories`). Los paquetes de terceros (`kobuki_core`, `kobuki_ros`, `kinect_ros2`, `libfreenect`, `depthimage_to_laserscan`, `cmd_vel_mux`, `velocity_smoother`) **no se incluyen como código**; sus instrucciones de instalación están documentadas en [`docs/02-software-setup.md`](docs/02-software-setup.md).

---

## Inicio rápido

Para replicar el proyecto completo, sigue las guías en `docs/` en orden numérico:

1. [Configuración de hardware](docs/01-hardware-setup.md)
2. [Instalación de software](docs/02-software-setup.md)
3. [Familiarización y control básico del Kobuki](docs/03-kobuki-basics.md)
4. [Integración del Kinect](docs/04-kinect-integration.md)
5. [Procesamiento de señales de sensores](docs/05-sensor-processing.md)
6. [Implementación de SLAM](docs/06-slam.md)
7. [Navegación autónoma](docs/07-navigation.md)

Si algo falla en el camino, revisa primero [`docs/troubleshooting.md`](docs/troubleshooting.md) — reúne los problemas reales encontrados durante el desarrollo y sus soluciones verificadas.

---

## Notas adicionales

Los scripts de trayectorias (`trayectoria_*.py`, `angulo_90.py`, `avanza_*.py`, `pruebas_*.py`) dentro de `kobuki_trajectories/` también se usaron para exportar datos cinemáticos (`.csv`) con fines de un modelado matemático, desarrollado como investigación independiente fuera del alcance de esta estadía.

## Autor

Estudiante: Christopher Jared Villa Alanis

Proyecto desarrollado como parte de una estadía profesional universitaria.

Repositorio: [SLAM_Documentacion](https://github.com/rocketant124/SLAM_Documentacion)
