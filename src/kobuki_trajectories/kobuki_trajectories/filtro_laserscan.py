#Utiliza funciones vectorizadas nativas de numpy (un filtro de mediana en bloque) que se ejecuta en milisegundos directamente en lenguaje C por debajo, 
#liberando por completo tu CPU:
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math
import numpy as np
from scipy.ndimage import median_filter # Requiere instalar scipy si no lo tienes

class FiltroLaserScan(Node):
    """
    Nodo de ROS 2 enfocado en el filtrado digital de alta velocidad
    para señales de LiDAR utilizando computación vectorial.
    """
    def __init__(self):
        super().__init__('filtro_laserscan')

        # Suscripción al tópico crudo del LiDAR
        self.sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # Publicador del flujo de datos depurado para SLAM y Nav2
        self.pub = self.create_publisher(LaserScan, '/scan_filtrado', 10)

        self.ventana = 5  # Tamaño de ventana del filtro (debe ser un número impar)

        self.get_logger().info('Filtro LaserScan iniciado...')

    def scan_callback(self, msg):

        # Conversión directa a arreglo de NumPy para habilitar vectorización
        # Convertir directamente a arreglo de numpy para velocidad
        ranges_np = np.array(msg.ranges)
        #ranges = list(msg.ranges)
        
        # Máscara booleana masiva para identificar lecturas de error físicas o lógicas
        # Reemplazar NaNs e Infinitos vectorialmente (sin bucles for)
        invalidos = np.isnan(ranges_np) | np.isinf(ranges_np) | (ranges_np <= 0)

        # Asignación vectorial rápida: Limpia errores seteándolos fuera de rango
        ranges_np[invalidos] = float('inf')
        
        # Aplicar filtro de mediana de forma masiva y ultra rápida
        # Usamos median_filter para procesar todo el vector en una sola línea de código ejecutable en C
        # Procesamiento en C: Filtro de mediana unidimensional en bloque masivo
        ranges_filtrados_np = median_filter(ranges_np, size=self.ventana, mode='nearest')
        
        # Consistencia de datos: Restaura los infinitos originales modificados por el filtro en los bordes
        # Devolver los infinitos donde el filtro haya puesto valores extraños por los bordes
        ranges_filtrados_np[np.isinf(ranges_np)] = float('inf')


        '''
        # usa float('inf') en lugar de 0.0 para los valores inválidos — eso es mejor porque slam_toolbox interpreta inf como "sin obstáculo" correctamente.
        ranges_limpios = [r if not math.isnan(r) and not math.isinf(r) and r > 0 else float('inf') for r in ranges]
        '''
        
        # Construcción y clonación de metadatos del mensaje de salida
        msg_filtrado = LaserScan()
        msg_filtrado.header = msg.header
        msg_filtrado.angle_min = msg.angle_min
        msg_filtrado.angle_max = msg.angle_max
        msg_filtrado.angle_increment = msg.angle_increment
        msg_filtrado.time_increment = msg.time_increment
        msg_filtrado.scan_time = msg.scan_time
        msg_filtrado.range_min = msg.range_min
        msg_filtrado.range_max = msg.range_max

        # Reconversión eficiente a lista estándar compatible con el formato del mensaje de ROS
        msg_filtrado.ranges = ranges_filtrados_np.tolist()
        msg_filtrado.intensities = []
        
        # Publicación del mensaje filtrado
        self.pub.publish(msg_filtrado)

def main():
    rclpy.init()
    node = FiltroLaserScan()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
