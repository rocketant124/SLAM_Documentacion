#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import time
import os  # Importante para mandar el comando de terminal

class LinealExperimentNode(Node):
    def __init__(self):
        super().__init__('pruebas_lineales')

        # Configurar únicamente el publicador para evitar bloqueos de red
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)

        # Leer velocidad desde los argumentos de la terminal (por defecto 0.15)
        self.v_cmd = 0.15
        if len(sys.argv) > 1:
            try:
                self.v_cmd = float(sys.argv[1])
            except ValueError:
                self.get_logger().error('Velocidad inválida. Usando 0.15 m/s por defecto.')

        self.get_logger().info(f'Configurado para prueba lineal a {self.v_cmd} m/s.')
        
        # --- SOLUCIÓN DE REINICIO FORZADO POR SISTEMA ---
        self.get_logger().info('Lanzando comando de reinicio de odometría del sistema...')
        # Ejecuta el llamado oficial directo en la terminal de Linux de fondo
        os.system("ros2 service call /commands/reset_odometry std_srvs/srv/Empty {} > /dev/null 2>&1 &")
        
        self.get_logger().info('Esperando 2 segundos de sincronización inicial y limpieza...')
        time.sleep(2.0)
        
        self.run_experiment()

    def run_experiment(self):
        self.get_logger().info('Odometría reiniciada. Iniciando fases del experimento...')
        msg = Twist()

        # 1. Mantener el robot detenido durante 2 segundos
        self.get_logger().info('Fase 1: Robot detenido (Registro inicial de 2s)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=2.0):
            msg.linear.x = 0.0
            self.publisher_.publish(msg)
            time.sleep(0.05)

        # 2. Aplicar la velocidad seleccionada durante 8 segundos
        self.get_logger().info(f'Fase 2: Aplicando velocidad de {self.v_cmd} m/s por 8s...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=8.0):
            msg.linear.x = self.v_cmd
            self.publisher_.publish(msg)
            time.sleep(0.05)

        # 3. Enviar velocidad cero y registrar durante 3 segundos adicionales
        self.get_logger().info('Fase 3: Comando cero enviado (Registro final de 3s)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=3.0):
            msg.linear.x = 0.0
            self.publisher_.publish(msg)
            time.sleep(0.05)

        self.get_logger().info('Prueba lineal finalizada con éxito.')

def main(args=None):
    rclpy.init(args=args)
    node = LinealExperimentNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()