'''from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():  
    # 1. Definir el argumento para recibir el mapa desde la terminal (map:=/ruta/mapa.yaml)
    map_yaml_file = LaunchConfiguration('map')

    declare_mapa_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=os.path.expanduser('~/mapa_laboratorio_two.yaml'),
        description='home/chris/mapa_laboratorio_two.yaml' #ruta del archivo yaml del mapa
    )
    
    # 2. Ruta de tus parámetros de Nav2 optimizados (donde está AMCL configurado)
    nav2_params = os.path.join(
        get_package_share_directory('kobuki_launch'),
        'config', 'nav2_params.yaml'
    )

    # 3. Llamar al bringup de Nav2 (Esto activa AMCL, Map Server y todo el ciclo de vida)  
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'),
                         'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': 'false',
            'params_file': nav2_params,
        }.items()
    )

    # 4. Configurar RViz2 apuntando a la carpeta de tu paquete
    rviz_config = os.path.join(
        get_package_share_directory('kobuki_launch'),
        'rviz', 'nav2_visualizador.rviz'
    )
    # Nodo de RViz2 cargando automaticamente la plantilla de topicos
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )
    
     # 5. Retornar la descripción del lanzamiento en el orden correcto
    return LaunchDescription([
        declare_mapa_yaml_cmd,
        nav2_launch,
        rviz,                      
    ])'''

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

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
        default_value=os.path.expanduser('~/mapa_pasillo.yaml'),
        description='home/chris/mapa_pasillo.yaml'
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

    return LaunchDescription([
        kobuki_kinect,
        declare_mapa,
        ekf_node,
        nav2_launch,
        relay_cmd_vel,
        rviz,
    ])



