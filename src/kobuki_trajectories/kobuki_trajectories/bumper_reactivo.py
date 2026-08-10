import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from kobuki_ros_interfaces.msg import BumperEvent

class BumperReactivo(Node):
    """
    Nodo de ROS 2 para navegación reactiva basada en eventos del bumper del Kobuki.
    Avanza en línea recta y ejecuta una maniobra de evitación (retroceder y girar)
    al detectar un colisión física.
    """
    def __init__(self):
        super().__init__('bumper_reactivo')

        # Publicador de comandos de velocidad a la base
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)

        # Suscriptor al evento del sensor de colisión físico (Bumper)
        self.sub = self.create_subscription(BumperEvent, '/events/bumper', self.bumper_callback, 10)

        # Bucle de control periódico a 10 Hz
        self.timer = self.create_timer(0.1, self.run)

        # Variables de control de estado y tiempo
        self.choque = False
        self.tiempo_choque = 0.0

        self.get_logger().info('Bumper reactivo iniciado...')

    def bumper_callback(self, msg):
        """Callback que se activa cuando el bumper cambia de estado (presionado/liberado)."""
        if msg.state == BumperEvent.PRESSED:
            self.get_logger().info(f'Choque detectado!')
            self.choque = True
            # Guarda la estampa de tiempo del momento del impacto
            self.tiempo_choque = self.get_clock().now().seconds_nanoseconds()[0]

    def run(self):
        """Bucle principal que ejecuta el comportamiento del robot según su estado."""
        msg = Twist()
        ahora = self.get_clock().now().seconds_nanoseconds()[0]

        if self.choque:
            if ahora - self.tiempo_choque < 1.0:

                # Retroceder durante 1.0 segundo
                msg.linear.x = -0.15
                msg.angular.z = 0.0
            elif ahora - self.tiempo_choque < 2.5:
                # Girar sobre su eje durante 1.5 segundos 
                msg.linear.x = 0.0
                msg.angular.z = 0.5
            else:
                # Reanudar marcha
                self.choque = False
        else:
            # Avanzar normalmente es decir en linea recta
            msg.linear.x = 0.15
            msg.angular.z = 0.0

        self.pub.publish(msg)

def main():
    rclpy.init()
    node = BumperReactivo()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
