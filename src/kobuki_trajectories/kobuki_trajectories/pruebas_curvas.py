#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class CurveExperimentNode(Node):
    def __init__(self):
        super().__init__('pruebas_curvas')
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)
        
        self.get_logger().info('Nodo de Trayectoria Curva Inicializado.')
        self.get_logger().info('Esperando 2 segundos de sincronización inicial...')
        time.sleep(2.0)
        
        self.run_experiment()

    def run_experiment(self):
        msg = Twist()

        # 1. Mantener el robot detenido durante 2 segundos
        self.get_logger().info('Fase 1: Robot detenido (Registro inicial de 2s)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=2.0):
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            time.sleep(0.05)

        # 2. Aplicar movimiento curvo simultáneo durante 12 segundos
        # v = 0.15 m/s, w = 0.20 rad/s -> Radio ideal = 0.75 m
        self.get_logger().info('Fase 2: Aplicando v=0.15 m/s y w=0.20 rad/s por 12s...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=12.0):
            msg.linear.x = 0.15
            msg.angular.z = 0.20
            self.publisher_.publish(msg)
            time.sleep(0.05)

        # 3. Enviar velocidad cero y registrar durante 3 segundos adicionales
        self.get_logger().info('Fase 3: Comando cero enviado (Registro final de 3s)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=3.0):
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            time.sleep(0.05)

        self.get_logger().info('Prueba de trayectoria curva finalizada con éxito.')

def main(args=None):
    rclpy.init(args=args)
    node = CurveExperimentNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()