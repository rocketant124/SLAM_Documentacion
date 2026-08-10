#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class RectangleTrajectoryNode(Node):
    def __init__(self):
        super().__init__('trayectoria_rectangulo')
        
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)
        
        self.get_logger().info('Nodo de trayectoria Rectangular inicializado.')
        self.get_logger().info('Esperando 2 segundos para la sincronización del ROS Bag...')
        time.sleep(2.0)
        
        self.run_experiment()

    def ejecutar_movimiento(self, v, w, segundos, descripcion):
        self.get_logger().info(descripcion)
        msg = Twist()
        msg.linear.x = v
        msg.angular.z = w
        
        start_time = self.get_clock().now()
        duration = rclpy.duration.Duration(seconds=segundos)
        
        while (self.get_clock().now() - start_time) < duration:
            self.publisher_.publish(msg)
            time.sleep(0.1)

    def run_experiment(self):
        # --- CONFIGURACIÓN DE VELOCIDADES ---
        v_avance = 0.15      # Velocidad lineal (m/s)
        w_giro = 0.3        # Velocidad angular (rad/s)
        t_giro_90 = 5.24    # Tiempo calculado para girar exactamente 90 grados
        # ------------------------------------

        # Lado 1: Avance largo (15s) + Giro 90°
        self.ejecutar_movimiento(v_avance, 0.0, 15.0, 'Tramo 1: Avanzando 15 segundos...')
        self.ejecutar_movimiento(0.0, w_giro, t_giro_90, 'Giro 1: Rotando 90° a la izquierda...')

        # Lado 2: Avance corto (3.5s) + Giro 90°
        self.ejecutar_movimiento(v_avance, 0.0, 4.0, 'Tramo 2: Avanzando 3.5 segundos...')
        self.ejecutar_movimiento(0.0, w_giro, t_giro_90, 'Giro 2: Rotando 90° a la izquierda...')

        # Lado 3: Avance largo (15s) + Giro 90°
        self.ejecutar_movimiento(v_avance, 0.0, 15.0, 'Tramo 3: Avanzando 15 segundos...')
        self.ejecutar_movimiento(0.0, w_giro, t_giro_90, 'Giro 3: Rotando 90° a la izquierda...')

        # Lado 4: Avance corto (3.5s) + Giro 90° para cerrar
        self.ejecutar_movimiento(v_avance, 0.0, 4.0, 'Tramo 4: Avanzando 3.5 segundos...')
        self.ejecutar_movimiento(0.0, w_giro, t_giro_90, 'Giro 4: Rotando 90° para cerrar el rectángulo...')

        # === DETENCIÓN DE SEGURIDAD ===
        self.get_logger().info('Trayectoria completada. Deteniendo el robot...')
        stop_msg = Twist()
        for _ in range(5):
            self.publisher_.publish(stop_msg)
            time.sleep(0.1)
            
        self.get_logger().info('Prueba finalizada con éxito.')

def main(args=None):
    rclpy.init(args=args)
    node = RectangleTrajectoryNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()