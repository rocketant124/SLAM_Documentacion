#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class GirarAngulo(Node):
    """
    Nodo de ROS 2 para realizar un giro en lazo cerrado monitoreando
    la orientación devuelta por la odometría del robot Kobuki.
    """
    def __init__(self):
        super().__init__('girar_angulo')

        # Publicador de velocidad para la base móvil        
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)

        # Suscriptor al flujo de odometría para retroalimentación de posición
        self.sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # Variables de estado angular
        self.yaw_inicio = None
        self.angulo_objetivo = 90.0  # Gira en grados

        # Pausa inicial opcional para asegurar la conexión de tópicos (p. ej. al usar ROS Bags)
        self.get_logger().info('Esperando 2 segundos para que el ROS Bag se conecte...')
        import time
        time.sleep(2.0)
        
        self.get_logger().info(f'Girando {self.angulo_objetivo} grados...')

    def odom_callback(self, msg):
        # Extracción de componentes del cuaternión en 2D    
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        # Conversión de Cuaternión a ángulo Yaw (grados sexagesimales)  
        yaw = math.degrees(math.atan2(2*qw*qz, 1 - 2*qz*qz))

        # Almacena la orientación inicial en la primera ejecución
        if self.yaw_inicio is None:
            self.yaw_inicio = yaw

        # Cálculo del ángulo girado acumulado
        angulo_girado = abs(yaw - self.yaw_inicio)

        # Corrección del salto de discontinuidad (+180 a -180 grados)
        if angulo_girado > 180:
            angulo_girado = 360 - angulo_girado

        cmd = Twist()

        # Control Lógico: Continúa girando si no ha alcanzado la meta
        if angulo_girado < self.angulo_objetivo:
            cmd.angular.z = 0.3 #Velocidad anglar en rad/s
            self.get_logger().info(f'Angulo girado: {angulo_girado:.1f}°')
        else:
            # Detención total y apagado seguro del nodo al cumplir la meta
            cmd.angular.z = 0.0
            self.pub.publish(cmd)
            self.get_logger().info('¡Giro completado!')
            rclpy.shutdown()
            return

        self.pub.publish(cmd)

def main():
    rclpy.init()
    node = GirarAngulo()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
