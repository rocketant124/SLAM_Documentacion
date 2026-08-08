from setuptools import find_packages, setup

package_name = 'kobuki_trajectories'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
	    'trayectoria_s = kobuki_trajectories.trayectoria_s:main',
	    'bumper_reactivo = kobuki_trajectories.bumper_reactivo:main',		
	    'leer_odometria = kobuki_trajectories.leer_odometria:main',
	    'mover_metro = kobuki_trajectories.mover_metro:main',
	    'angulo_90 = kobuki_trajectories.angulo_90:main',  
        'trayectoria_cuadro = kobuki_trajectories.trayectoria_cuadro:main',
        'cuadrado_odom = kobuki_trajectories.cuadrado_odom:main',
        'evasion_obstaculos = kobuki_trajectories.evasion_obstaculos:main',
        'filtro_laserscan = kobuki_trajectories.filtro_laserscan:main',
        'avanza_5s = kobuki_trajectories.avanza_5s:main',
        'avanza_15s = kobuki_trajectories.avanza_15s:main',
        'trayectoria_infinito = kobuki_trajectories.trayectoria_infinito:main',
        'trayectoria_zigzag = kobuki_trajectories.trayectoria_zigzag:main',
        'trayectoria_rectangulo = kobuki_trajectories.trayectoria_rectangulo:main',
        'pruebas_lineales = kobuki_trajectories.pruebas_lineales:main',
        'pruebas_angulares = kobuki_trajectories.pruebas_angulares:main',
        'cambio_velocidad = kobuki_trajectories.cambio_velocidad:main',
        'pruebas_curvas = kobuki_trajectories.pruebas_curvas:main',
        ],
    },
)
