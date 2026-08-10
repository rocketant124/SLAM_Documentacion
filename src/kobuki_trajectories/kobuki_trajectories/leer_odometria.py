import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class LeerOdometria(Node):
    def __init__(self):
        super().__init__('leer_odometria')
        self.sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.get_logger().info('Leyendo odometría...')

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        
        # Convertir quaternion a angulo yaw
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        yaw = math.atan2(2*qw*qz, 1 - 2*qz*qz)
        yaw_grados = math.degrees(yaw)
        
        self.get_logger().info(
            f'Posicion -> X: {x:.3f}m  Y: {y:.3f}m  Angulo: {yaw_grados:.1f}°'
        )

def main():
    rclpy.init()
    node = LeerOdometria()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
