#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class ZigZagTrajectoryNode(Node):
    def __init__(self):
        super().__init__('trayectoria_zigzag')
        
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)
        
        self.get_logger().info('Nodo de trayectoria en Zig-Zag inicializado.')
        self.get_logger().info('Esperando 2 segundos para la sincronización del ROS Bag...')
        time.sleep(2.0)
        
        self.run_experiment()

    def run_experiment(self):
        msg = Twist()
        
        # --- PARÁMETROS DEL ZIG-ZAG ---
        v_lineal = 0.15     # Velocidad constante de avance (m/s)
        w_angular = 0.4     # Velocidad angular de giro (rad/s)
        duracion_tramo = 4.0 # Segundos por cada diagonal
        # ------------------------------

        # Arreglo con los signos del giro: [Izquierda, Derecha, Izquierda, Derecha]
        pasos = [1, -1, 1, -1]
        
        for i, signo in enumerate(pasos):
            direccion = "IZQUIERDA" if signo == 1 else "DERECHA"
            self.get_logger().info(f'Iniciando Tramo {i+1}: Avance con giro a la {direccion}...')
            
            msg.linear.x = v_lineal
            msg.angular.z = w_angular * signo
            
            start_time = self.get_clock().now()
            duration = rclpy.duration.Duration(seconds=duracion_tramo)
            
            while (self.get_clock().now() - start_time) < duration:
                self.publisher_.publish(msg)
                time.sleep(0.1)

        # === DETENCIÓN DE SEGURIDAD ===
        self.get_logger().info('Trayectoria en Zig-Zag completada. Deteniendo el robot...')
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        
        for _ in range(5):
            self.publisher_.publish(stop_msg)
            time.sleep(0.1)
            
        self.get_logger().info('Prueba finalizada.')

def main(args=None):
    rclpy.init(args=args)
    node = ZigZagTrajectoryNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()