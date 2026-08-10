#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import time
from std_srvs.srv import Empty 

class AngularExperimentNode(Node):
    def __init__(self):
        super().__init__('pruebas_angulares')

          # Configurar el cliente del servicio y el publicador primero
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)
        self.cli = self.create_client(Empty, '/reset_odometry')

        # Esperar a que el servicio esté disponible
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servicio /reset_odometry...')

        # Valores por defecto si no se envían argumentos
        self.w_cmd = 0.20
        
        if len(sys.argv) > 1:
            try:
                self.w_cmd = float(sys.argv[1])
            except ValueError:
                self.get_logger().error('Velocidad angular inválida. Usando 0.20 rad/s por defecto.')

        self.get_logger().info(f'Configurado para prueba angular a {self.w_cmd} rad/s.')
        self.get_logger().info('Esperando 2 segundos de sincronización inicial...')
        time.sleep(2.0)
        
        self.run_experiment()

    def run_experiment(self):

        # Llamar al servicio de forma síncrona para resetear antes de iniciar
        self.get_logger().info('Enviando solicitud de reinicio de odometría...')
        req = Empty.Request()

        # Usamos una llamada del futuro que espere a que el servicio responda
        future = self.cli.call_async(req)
        # Forzamos a ROS a procesar esta llamada específica antes de avanzar
        rclpy.spin_until_future_complete(self, future) #Esta línea bloquea el script de manera segura durante una fracción de milisegundo, obligando a ROS 2 a procesar la comunicación del servicio /reset_odometry.

        self.get_logger().info('Odometría reiniciada a cero con éxito.')

        msg = Twist()

        # 1. Mantener el robot detenido durante 2 segundos
        self.get_logger().info('Fase 1: Robot detenido (Registro inicial de 2s)...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=2.0):
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            time.sleep(0.05)

        # 2. Aplicar la velocidad angular seleccionada durante 7 segundos
        self.get_logger().info(f'Fase 2: Aplicando velocidad angular de {self.w_cmd} rad/s por 7s...')
        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time) < rclpy.duration.Duration(seconds=7.0):
            msg.linear.x = 0.0
            msg.angular.z = self.w_cmd
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

        self.get_logger().info('Prueba angular finalizada con éxito.')

def main(args=None):
    rclpy.init(args=args)
    node = AngularExperimentNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()