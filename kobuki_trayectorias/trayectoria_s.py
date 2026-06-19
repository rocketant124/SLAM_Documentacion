import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TrayectoriaS(Node):
    """
    Nodo de ROS 2 para ejecutar una trayectoria en 'S' de forma abierta
    en una base móvil Kobuki.
    """
    def __init__(self):
        super().__init__('trayectoria_s')

        # Publicador para los comandos de velocidad de la base Kobuki
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)

        # Temporizador del bucle de control (10 Hz)
        self.timer = self.create_timer(0.1, self.run)

        # Variables de control de tiempo y estado
        self.inicio = time.time()
        self.fase = 0
        self.get_logger().info('Iniciando trayectoria S...')

    def run(self):
        msg = Twist()
        # Calcula el tiempo transcurrido en la fase actual
        t = time.time() - self.inicio

        # FASE 0: Primera curva cerrada (Izquierda)
        if self.fase == 0:
            msg.linear.x = 0.15 # m/s
            msg.angular.z = 0.5 # rad/s
            if t > 3.0:
                self.fase = 1
                self.inicio = time.time() # Reinicia el cronómetro para la siguiente fase
                self.get_logger().info('Segunda curva...')

        # FASE 1: Segunda curva cerrada (Derecha)
        elif self.fase == 1:
            msg.linear.x = 0.15 # m/s
            msg.angular.z = -0.5 # rad/s
            if t > 3.0:
                self.fase = 2
                self.get_logger().info('Completado!')

        # FASE 2: Parada de emergencia y apagado del nodo
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.pub.publish(msg)
            rclpy.shutdown()
            return

        # Publica el comando de velocidad calculado
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = TrayectoriaS()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
