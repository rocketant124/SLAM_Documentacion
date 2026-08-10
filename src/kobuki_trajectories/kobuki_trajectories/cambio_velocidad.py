#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class SpeedChangeExperimentNode(Node):
    def __init__(self):
        super().__init__('cambio_velocidad')

        # Configurar el cliente del servicio y el publicador primero
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)
            
        
        self.get_logger().info('Nodo de Cambio de Velocidad en Escalón Inicializado.')
        self.get_logger().info('Esperando 2 segundos de sincronización inicial...')
        time.sleep(2.0)
        
        self.run_experiment()

    def run_experiment(self):

        msg = Twist()

        # Etapa 1: Detenido de 0 <= t < 2
        self.get_logger().info('Etapa 1: Detenido (0s a 2s)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=2.0):
            msg.linear.x = 0.0
            self.publisher_.publish(msg)
            time.sleep(0.05)

        # Etapa 2: Primer nivel de velocidad (0.10 m/s) de 2 <= t < 6
        self.get_logger().info('Etapa 2: Primer nivel (0.10 m/s de 2s a 6s)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=4.0):
            msg.linear.x = 0.10
            self.publisher_.publish(msg)
            time.sleep(0.05)

        # Etapa 3: Segundo nivel de velocidad (0.20 m/s) de 6 <= t < 10
        self.get_logger().info('Etapa 3: Segundo nivel (0.20 m/s de 6s a 10s)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=4.0):
            msg.linear.x = 0.20
            self.publisher_.publish(msg)
            time.sleep(0.05)

        # Etapa 4: Detención y registro final t >= 10 (por 3 segundos adicionales)
        self.get_logger().info('Etapa 4: Detención total (Registro final)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=3.0):
            msg.linear.x = 0.0
            self.publisher_.publish(msg)
            time.sleep(0.05)

        self.get_logger().info('Prueba de cambio de velocidad finalizada.')

def main(args=None):
    rclpy.init(args=args)
    node = SpeedChangeExperimentNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()