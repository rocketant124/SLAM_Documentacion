from setuptools import find_packages, setup

package_name = 'kobuki_launch'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
       	('share/' + package_name + '/launch', [
            'launch/kobuki_kinect.launch.py',
	        'launch/slam.launch.py',
            'launch/navegacion.launch.py',
    ]),
        ('share/' + package_name + '/config', [
            'config/nav2_params.yaml',
            'config/ekf_config.yaml',
            'config/laserscan_config.yaml',
            'config/mapper_params_online_async.yaml',
    ]),
        ('share/' + package_name + '/rviz', [
            'rviz/navegacion.rviz',
            'rviz/mapeo.rviz',
    ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chris',
    maintainer_email='chris@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
