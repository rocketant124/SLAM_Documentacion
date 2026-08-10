import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class CuadradoOdom(Node):
    """
    Nodo de ROS 2 para trazar un cuadrado en lazo cerrado utilizando la retroalimentación
    de posición (X, Y) y orientación (Yaw) del tópico de odometría (/odom).
    """
    def __init__(self):
        super().__init__('cuadrado_odom')

        # Publicador de comandos de velocidad para la base Kobuki
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)

        # Suscriptor al flujo de odometría para retroalimentación en tiempo real
        self.sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # Dos estados; avanzar o girar
        self.fase = 'avanzar'
        self.lado = 0

        # Memorización de puntos de referencia iniciales
        self.x_inicio = None
        self.y_inicio = None
        self.yaw_inicio = None

        self.distancia_objetivo = 0.4  # Metros por lado 
        self.angulo_objetivo = 90.0    # Grados en esquina 
        self.get_logger().info('Iniciando cuadrado con odometría...')

    def get_yaw(self, msg):
        """Calcula el ángulo Yaw en grados sexagesimales a partir del cuaternión en 2D."""
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        return math.degrees(math.atan2(2*qw*qz, 1 - 2*qz*qz))

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        yaw = self.get_yaw(msg)

        cmd = Twist()

        # Condicion la trayectoria finaliza tras completar los 4 lados
        if self.lado >= 4:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.pub.publish(cmd)
            self.get_logger().info('¡Cuadrado completado!')
            rclpy.shutdown()
            return

        # Avanza en linea recta hasta alcanzar las distancia euclidiana objetivo
        if self.fase == 'avanzar':
            if self.x_inicio is None:
                self.x_inicio = x
                self.y_inicio = y

            # Distancia euclidiana recorrida desde el inicio del lado actual
            distancia = math.sqrt((x - self.x_inicio)**2 + (y - self.y_inicio)**2)
            self.get_logger().info(f'Lado {self.lado+1} - Distancia: {distancia:.3f}m')

            if distancia < self.distancia_objetivo:
                cmd.linear.x = 0.15
            else:
                # Transición a la fase de giro y reseteo de referencias
                self.fase = 'girar'
                self.x_inicio = None
                self.y_inicio = None
                self.yaw_inicio = None

        # E robor gira sobre el eje z hasta alcanzar los 90 grados
        elif self.fase == 'girar':
            if self.yaw_inicio is None:
                self.yaw_inicio = yaw

            angulo_girado = abs(yaw - self.yaw_inicio)
            if angulo_girado > 180:
                angulo_girado = 360 - angulo_girado

            self.get_logger().info(f'Giro {self.lado+1} - Angulo: {angulo_girado:.1f}°')

            if angulo_girado < self.angulo_objetivo:
                cmd.angular.z = 0.3
            else:
                # Transición a la siguiente recta e incremento del contador de lados
                self.fase = 'avanzar'
                self.lado += 1
                self.yaw_inicio = None

        self.pub.publish(cmd)

def main():
    rclpy.init()
    node = CuadradoOdom()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
