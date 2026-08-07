from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

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

    # SLAM Toolbox
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('slam_toolbox'),
                         'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'false',
            'slam_params_file': '/home/chris/mapper_params_online_async.yaml' # Archivo personalizado
        }.items()
    )

    # RViz2 para visualizar el mapa

    # Ruta a configuracion de rviz
    rviz_config = os.path.join(
        get_package_share_directory('kobuki_launch'),
        'rviz', 'mapeo.rviz'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
    )

    return LaunchDescription([
        kobuki_kinect,
        ekf_node,
        slam,
        rviz,
    ])
