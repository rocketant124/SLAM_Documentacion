#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class InfiniteTrajectoryNode(Node):
    def __init__(self):
        super().__init__('trayectoria_infinito')
        
        # Publicador al tópico del driver del Kobuki
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)
        
        self.get_logger().info('Nodo de trayectoria en Infinito inicializado.')
        self.get_logger().info('Esperando 2 segundos para la sincronización del ROS Bag...')
        time.sleep(2.0)
        
        self.run_experiment()

    def run_experiment(self):
        msg = Twist()
        
        # --- PARÁMETROS DE LA TRAYECTORIA ---
        # Definimos una velocidad lineal constante para todo el recorrido
        v_lineal = 0.15  # m/s
        # Definimos la velocidad angular de giro
        w_angular = 0.3  # rad/s
        
        # Para hacer un círculo completo (2*pi radianes) a una velocidad w:
        # Tiempo = (2 * pi) / w  ->  6.2831 / 0.3 = ~20.94 segundos
        tiempo_circulo = 20.94
        # -------------------------------------

        # === FASE 1: CÍRCULO HACIA LA IZQUIERDA ===
        self.get_logger().info('Iniciando Fase 1: Giro hacia la IZQUIERDA...')
        msg.linear.x = v_lineal
        msg.angular.z = w_angular  # Positivo = Antihorario (Izquierda)
        
        start_time = self.get_clock().now()
        duration = rclpy.duration.Duration(seconds=tiempo_circulo)
        
        while (self.get_clock().now() - start_time) < duration:
            self.publisher_.publish(msg)
            time.sleep(0.1)

        # === FASE 2: CÍRCULO HACIA LA DERECHA ===
        self.get_logger().info('Iniciando Fase 2: Giro hacia la DERECHA...')
        msg.linear.x = v_lineal
        msg.angular.z = -w_angular  # Negativo = Horario (Derecha)
        
        start_time = self.get_clock().now()
        
        while (self.get_clock().now() - start_time) < duration:
            self.publisher_.publish(msg)
            time.sleep(0.1)

        # === DETENCIÓN DE SEGURIDAD ===
        self.get_logger().info('Trayectoria en infinito completada. Deteniendo el robot...')
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        
        for _ in range(5):
            self.publisher_.publish(stop_msg)
            time.sleep(0.1)
            
        self.get_logger().info('Prueba finalizada.')

def main(args=None):
    rclpy.init(args=args)
    node = InfiniteTrajectoryNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()