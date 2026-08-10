from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

'''
----------------------------------------------------------------------------------------------------------------------------------------------------------------  
| Aqui se encuentran los nodos para complementar los procesos que debe hacer el kinect 
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

def generate_launch_description():

    # 1. Nodo de la Kobuki (Silenciando su TF si el EKF la va a publicar)
    kobuki_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('kobuki_node'),
                         'launch', 'kobuki_node-launch.py')
        ),
    )

    # 2. CONFIGURACIÓN LIMPIA DE LA KINECT (En lugar del launch genérico)
    kinect_node = Node(
        package='kinect_ros2',
        executable='kinect_ros2_node',
        name='kinect_ros2',
        namespace='kinect', # Esto hace el --remap __ns:=/kinect
        parameters=[{
            'fps': 10,
            'depth_registration': False
        }]
    )

    # 3. Transformadas Estática (Conectando base_footprint con el namespace de tu kinect)
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='kinect_tf',
        arguments=['0.1', '0', '0.3', '0', '0', '0', 'base_footprint', 'kinect_depth']
    )

    # 3. Transformadas de camera "depth_frame"
    static_tf_camera = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='kinect_depth_tf',
        arguments=['0', '0', '0', '0', '0', '0', 'kinect_depth', 'camera_depth_frame']
    )

    # 3. Transformadas de baselink
    static_tf_baselink = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_tf',
        arguments=['0', '0', '0', '0', '0', '0', 'base_footprint', 'base_link']
    )


    # Obtener el directorio share de tu paquete
    pkg_kobuki_launch = get_package_share_directory('kobuki_launch')

    # 4. Convertidor de Imagen de Profundidad a Láser 2D
    laserscan_config = os.path.join(
    pkg_kobuki_launch, 'config', 'laserscan_config.yaml'
    )

    depthimage_to_laserscan = Node(
        package='depthimage_to_laserscan',
        executable='depthimage_to_laserscan_node',
        name='depthimage_to_laserscan',
        parameters=[laserscan_config],
        remappings=[
            ('depth', '/kinect/depth/image_raw'),
            ('depth_camera_info', '/kinect/depth/camera_info'),
            ('scan', '/scan')
        ]
    )

    
    return LaunchDescription([
        kobuki_launch,
        kinect_node,  #Nodo optimizado
        static_tf,
        static_tf_camera,
        static_tf_baselink,
        depthimage_to_laserscan,
    ])