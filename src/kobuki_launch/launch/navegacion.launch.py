#Librerias a usar
from launch import LaunchDescription # Launch Framework principal que agrupa todos los nodos y aciones que se ejecutarán y LaunchDescription es la acción para incluir y ejecutar un archivo de lanzamiento dentro de otro
from launch_ros.actions import Node  # Importa la acción para lanzar nodos individuales de ROS 2
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument # Importa las acciones para incluir otros archivos launch y declarar argumentos
from launch.launch_description_sources import PythonLaunchDescriptionSource # Importa el cargador para interpretar archivos de lanzamiento basados en Python
from launch.substitutions import LaunchConfiguration # Importa la herramienta para recuperar los valores de los argumentos de lanzamiento
from ament_index_python.packages import get_package_share_directory # Importa la función para encontrar la ruta instalada de un paquete ROS 2
import os # Importa la librería estándar de Python para interactuar con el sistema de archivos

def generate_launch_description():

    # Kobuki + Kinect
    kobuki_kinect = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('kobuki_launch'),
                         'launch', 'kobuki_kinect.launch.py')
        )
    )

    mapa_config = LaunchConfiguration('mapa')

    declare_mapa = DeclareLaunchArgument(
        'mapa',
        default_value=os.path.expanduser('~/mapa_laboratorio_two.yaml'),
        description='home/chris/mapa_laboratorio_two.yaml'
    )

    nav2_params = os.path.join(
        get_package_share_directory('kobuki_launch'),
        'config', 'nav2_params.yaml'
    )

    # Nav2 Bringup (Lanza AMCL, Planners y Lifecycle)
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'),
                         'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': mapa_config,
            'use_sim_time': 'false',
            'params_file': nav2_params,
            'autostart': 'true', # Levanta los nodos de Nav2 automáticamente
        }.items()
    )

    '''
    #Usar este código, en caso de que se presenten, inestabilidades en el funcionamiento del robot
    
    # Retrasar Nav2 por 4.0 segundos
    nav2_delayed = TimerAction(
        period=4.0,
        actions=[nav2_launch]
    )
    '''

    # Filtro de Kalman (EKF)
    ekf_config = os.path.join(
        get_package_share_directory('kobuki_launch'),
        'config', 'ekf_config.yaml'
    )

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        parameters=[
            ekf_config,
            {'use_sim_time': False}
        ],
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

    # Puente de Velocidades Nativo (Reemplaza al .sh)
    relay_cmd_vel = Node(
        package='topic_tools',
        executable='relay',
        name='relay_cmd_vel',
        output='screen',
        arguments=['/cmd_vel', '/commands/velocity']
    )

    # RViz2 con soporte nativo
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(get_package_share_directory('nav2_bringup'), 'rviz', 'nav2_default_view.rviz')]
    )

    '''
    #Usar este código, en caso de que se presenten, inestabilidades en el funcionamiento del robot

    # Retrasar RViz2 por 7.0 segundos
    rviz_delayed = TimerAction(
        period=7.0,
        actions=[rviz_node]
    )
    '''

    return LaunchDescription([
        kobuki_kinect,
        declare_mapa,
        ekf_node,
        nav2_launch,
        relay_cmd_vel,
        rviz,
    ])

'''
#Si deseas utilizar los retrasos en caso de intestabilidad, el return LaunchDescription, quedaria:

    return LaunchDescription([
        kobuki_kinect,
        declare_mapa,
        relay_cmd_vel,
        ekf_delayed,   # t = 1.5s
        nav2_delayed,  # t = 4.0s
        rviz_delayed,  # t = 7.0s
    ])
'''

