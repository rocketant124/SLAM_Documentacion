import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class MoverDistancia(Node):
    """
    Nodo de ROS 2 para desplazar el robot Kobuki una distancia recta fija 
    utilizando retroalimentación de posición en lazo cerrado desde el tópico /odom.
    """
    def __init__(self):
        super().__init__('mover_distancia')

        # Publicador de comandos de velocidad a la base
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)

        # Suscriptor al flujo de odometría para el cálculo de distancia
        self.sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # Coordenadas origen
        self.x_inicio = None
        self.y_inicio = None

        # Meta de desplazamiento
        self.distancia_objetivo = 1.0  # metros
        self.get_logger().info(f'Avanzando {self.distancia_objetivo} metros...')

    def odom_callback(self, msg):
        """Calcula la distancia recorrida mediante la fórmula de distancia euclidiana 2D."""
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # Registra la posición inicial al recibir la primera lectura del sensor
        if self.x_inicio is None:
            self.x_inicio = x
            self.y_inicio = y

        # Distancia euclidiana recorrida respecto al punto de partida (m)
        distancia = math.sqrt((x - self.x_inicio)**2 + (y - self.y_inicio)**2)

        cmd = Twist()

        # Continua avanzando hasta que alcance el objetivo 
        if distancia < self.distancia_objetivo:
            cmd.linear.x = 0.15
            self.get_logger().info(f'Distancia recorrida: {distancia:.3f}m')
        else:
            # El robot frena y se apaga el nodo
            cmd.linear.x = 0.0
            self.pub.publish(cmd)
            self.get_logger().info('¡Objetivo alcanzado!')
            rclpy.shutdown()
            return

        self.pub.publish(cmd)

def main():
    rclpy.init()
    node = MoverDistancia()
    rclpy.spin(node)

if __name__ == '__main__':
    main()

