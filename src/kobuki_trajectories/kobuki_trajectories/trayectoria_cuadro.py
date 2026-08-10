import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TrayectoriaCuadro(Node):
    """
    Nodo de ROS 2 para trazar una trayectoria cuadrada mediante una máquina 
    de estados no bloqueante basada en temporizadores (10 Hz) y control en lazo abierto.
    """
    def __init__(self):
        super().__init__('trayectoria_cuadro')

        # Publicador de comandos de velocidad para la base Kobuki
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)

        # Bucle de control periódico asíncrono (10 Hz)
        self.timer = self.create_timer(0.1, self.run)

        # Control de estado, tiempo y contador de lados
        self.inicio = time.time()
        self.fase = 0 # 0 : Avanza recto, 1: Girar
        self.lado = 0 # Contador de lados completados
        self.get_logger().info('Iniciando cuadrado...')

    def run(self):
        msg = Twist()
        t = time.time() - self.inicio

        # Condicion que se activa al completar el cuadrado
        if self.lado >= 4:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.pub.publish(msg)
            self.get_logger().info('Cuadrado completado!')
            rclpy.shutdown()
            return

        # Avanzar en línea recta (0.2 m/s * 2.0 s = 0.4 metros)
        if self.fase == 0:  # Avanzar recto
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            if t > 2.0:
                self.fase = 1
                self.inicio = time.time()

        # Giro sobre el propio eje (0.5 rad/s * 3.0 s = 1.5 rad ≈ 86°)
        elif self.fase == 1:  # Girar 90 grados
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            if t > 3.0:
                self.fase = 0
                self.lado += 1
                self.inicio = time.time()
                self.get_logger().info(f'Lado {self.lado} completado')

        # Publicación del comando de velocidad actual
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = TrayectoriaCuadro()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
