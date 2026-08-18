#Librerias a usar
from launch import LaunchDescription # Launch Framework principal que agrupa todos los nodos y aciones que se ejecutarán y LaunchDescription es la acción para incluir y ejecutar un archivo de lanzamiento dentro de otro
from launch_ros.actions import Node  # Importa la acción para lanzar nodos individuales de ROS 2
from launch.actions import IncludeLaunchDescription 
from launch.launch_description_sources import PythonLaunchDescriptionSource # Importa el cargador para interpretar archivos de lanzamiento basados en Python
from ament_index_python.packages import get_package_share_directory # Importa la función para encontrar la ruta instalada de un paquete ROS 2
import os # Importa la librería estándar de Python para interactuar con el sistema de archivos
from launch.actions import IncludeLaunchDescription, TimerAction # Se agrega TimerAction para meter retrasos de arranque

'''
----------------------------------------------------------------------------------------------------------------------------------------------------------------
| En la primera seccion se encuentra el direccionamiento a kobuki_kinect.launch.py en donde estan cargados los nodos de este mismo. 
|    
| Nodos que encuentras este archivo "slam.launch.py: nodo de ekf, el nodo que carga a slam_toolbox y una configuracion de rviz con los displays que se ocuparan.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

def generate_launch_description():

    # Kobuki + Kinect
    kobuki_kinect = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('kobuki_launch'),
                         'launch', 'kobuki_kinect.launch.py')
        )
    )
    
    ekf_config = os.path.join(
    get_package_share_directory('kobuki_launch'),
    'config', 'ekf_config.yaml'
    )

    ekf_node = Node(
    package='robot_localization',
    executable='ekf_node',
    name='ekf_filter_node',
    parameters=[ekf_config],
    remappings=[('odometry/filtered', '/odom_filtered')]
    )

    '''
    #Usar este código, en caso de que se presenten, inestabilidades en el funcionamiento del robot
    
    # Retrasar EKF por 1.5 segundos (para dar tiempo a que los sensores publiquen)
    ekf_delayed = TimerAction(
        period=1.5,
        actions=[ekf_node]
    )
    '''

    # Obtener la ruta del directorio share de tu paquete
    pkg_kobuki_launch = get_package_share_directory('kobuki_launch')

    # Construir la ruta relativa al archivo YAML en la carpeta config
    mapper_params_file = os.path.join(pkg_kobuki_launch, 'config', 'mapper_params_online_async.yaml')

    # SLAM Toolbox
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('slam_toolbox'),
                         'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'false',
            'slam_params_file': mapper_params_file # Archivo personalizado, usamos la variable que guarda la ruta del .yaml
        }.items()
    )

    '''
    #Usar este código, en caso de que se presenten, inestabilidades en el funcionamiento del robot

    # 2. Retrasar SLAM Toolbox por 3.0 segundos
    slam_delayed = TimerAction(
        period=3.0,
        actions=[slam_toolbox_launch]
    )
    '''
    
    # RViz2 para visualizar el mapa
    # Ruta a configuracion de rviz
    rviz_config = os.path.join(
        get_package_share_directory('kobuki_launch'),
        'rviz', 'mapeo.rviz'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
    )

    '''
    #Usar este código, en caso de que se presenten, inestabilidades en el funcionamiento del robot

    # 3. Retrasar RViz2 por 5.0 segundos (para que SLAM ya esté listo)
    rviz_delayed = TimerAction(
        period=5.0,
        actions=[rviz_node]
    )
    '''
    return LaunchDescription([
        kobuki_kinect,
        ekf_node,
        slam_toolbox_launch,
        rviz_node,
    ])

'''
#Si deseas utilizar los retrasos en caso de intestabilidad, el return LaunchDescription, quedaria:

    return LaunchDescription([
        kobuki_kinect,
        ekf_delayed,
        slam_delayed,
        rviz_delayed,
    ])
'''