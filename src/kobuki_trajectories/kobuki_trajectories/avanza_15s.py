#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class KobukiCharacterizationNode(Node):
    def __init__(self):
        super().__init__('kobuki_characterization')
        
        # Publicador al tópico estándar de velocidad del robot
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)
        
        # Esperamos un momento a que la conexión con el robot se establezca bien
        self.get_logger().info('Nodo de caracterización inicializado. Preparando motores...')
        time.sleep(2.0) 
        
        self.run_experiment()

    def run_experiment(self):
        msg = Twist()
        
        # --- CONFIGURACIÓN DE LA PRUEBA ---
        # Definimos una velocidad lineal constante (15 cm/s) y angular en 0 (Línea recta)
        msg.linear.x = 0.15 
        msg.angular.z = 0.0
        duracion_segundos = 15.0
        # ----------------------------------

        self.get_logger().info(f'Iniciando movimiento: v = {msg.linear.x} m/s por {duracion_segundos} segundos.')
        
        # Guardamos el tiempo de inicio de forma correcta usando el reloj de ROS 2
        start_time = self.get_clock().now()
        
        # Convertimos la duración esperada a un objeto Duration de rclpy
        duration = rclpy.duration.Duration(seconds=duracion_segundos)

        # Publicamos continuamente dentro del periodo de tiempo
        while (self.get_clock().now() - start_time) < duration:
            self.publisher_.publish(msg)
            # Publicamos a una frecuencia aproximada de 10 Hz (cada 100 ms)
            time.sleep(0.1)

        # --- DETENCIÓN DE SEGURIDAD ---
        self.get_logger().info('Tiempo cumplido. Deteniendo el robot...')
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        
        # Publicamos el mensaje de parada varias veces para asegurar que el robot lo reciba
        for _ in range(5):
            self.publisher_.publish(stop_msg)
            time.sleep(0.1)
            
        self.get_logger().info('Prueba finalizada con éxito.')

def main(args=None):
    rclpy.init(args=args)
    node = KobukiCharacterizationNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()