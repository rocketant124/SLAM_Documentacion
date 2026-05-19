import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from kobuki_ros_interfaces.msg import BumperEvent

class BumperReactivo(Node):
    def __init__(self):
        super().__init__('bumper_reactivo')
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)
        self.sub = self.create_subscription(BumperEvent, '/events/bumper', self.bumper_callback, 10)
        self.timer = self.create_timer(0.1, self.run)
        self.choque = False
        self.tiempo_choque = 0.0
        self.get_logger().info('Bumper reactivo iniciado...')

    def bumper_callback(self, msg):
        if msg.state == BumperEvent.PRESSED:
            self.get_logger().info(f'Choque detectado!')
            self.choque = True
            self.tiempo_choque = self.get_clock().now().seconds_nanoseconds()[0]

    def run(self):
        msg = Twist()
        ahora = self.get_clock().now().seconds_nanoseconds()[0]

        if self.choque:
            if ahora - self.tiempo_choque < 1.0:
                # Retroceder
                msg.linear.x = -0.15
                msg.angular.z = 0.0
            elif ahora - self.tiempo_choque < 2.5:
                # Girar
                msg.linear.x = 0.0
                msg.angular.z = 0.5
            else:
                # Reanudar marcha
                self.choque = False
        else:
            # Avanzar normalmente
            msg.linear.x = 0.15
            msg.angular.z = 0.0

        self.pub.publish(msg)

def main():
    rclpy.init()
    node = BumperReactivo()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
