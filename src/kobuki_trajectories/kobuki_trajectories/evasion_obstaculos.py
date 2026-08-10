import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class EvasionObstaculosAvanzada(Node):
    def __init__(self):
        super().__init__('evasion_obstaculos_avanzada')
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)
        self.sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # Umbrales de distancia
        self.distancia_critica = 0.41   # MENOS de esto = ¡Peligro de choque! Modo pánico.
        self.distancia_minima = 0.65    # Distancia normal para empezar a esquivar.
        self.distancia_despejado = 0.95  # El frente debe estar MUY libre para dejar de girar.
        
        # Velocidades
        self.velocidad_lineal = 0.15
        self.velocidad_angular = 0.5
        
        # Estados: 'avanzar', 'girando_evasion', 'retrocediendo'
        self.estado = 'avanzar'
        self.direccion_giro = 0.0 
        
        self.get_logger().info('Evasión Avanzada iniciada. Sistema antibucles activo...')

    def scan_callback(self, msg):
        ranges = msg.ranges
        total = len(ranges)
        
        tercio = total // 3
        zona_izquierda = ranges[:tercio]
        zona_centro = ranges[tercio:2*tercio]
        zona_derecha = ranges[2*tercio:]
        
        def min_valido(zona):
            vals = [r for r in zona if not math.isnan(r) and not math.isinf(r) and r > 0]
            return min(vals) if vals else float('inf')
        
        dist_izq = min_valido(zona_izquierda)
        dist_centro = min_valido(zona_centro)
        dist_der = min_valido(zona_derecha)
        dist_total = dist_izq+dist_centro+dist_der
        
        cmd = Twist()
        
        # =========================================================================
        # MÁQUINA DE ESTADOS ANTIBUCLES
        # =========================================================================
        
        # CASO 1: MODO PÁNICO (El robot no tuvo tiempo de frenar o el objeto es enorme)
        if dist_total < self.distancia_critica:
            self.estado = 'retrocediendo'
            cmd.linear.x = -0.35  # Marcha atrás
            # Gira en dirección contraria al obstáculo más cercano mientras retrocede
            cmd.angular.z = self.velocidad_angular if dist_izq > dist_der else -self.velocidad_angular
            
        # CASO 2: SEGUIR GIRANDO (Si ya estábamos esquivando, no paramos hasta que esté MUY despejado)
        elif self.estado == 'girando_evasion':
            if dist_centro < self.distancia_despejado:
                # Mantenemos el giro de evasión de forma estricta
                cmd.linear.x = 0.0
                cmd.angular.z = self.direccion_giro
            else:
                # Por fin se despejó por completo el frente
                self.estado = 'avanzar'
                
        # CASO 3: DETECTAR NUEVO OBSTÁCULO DE FRENTE
        elif dist_centro < self.distancia_minima:
            self.estado = 'girando_evasion'
            # Elegimos el lado más libre y lo congelamos en 'self.direccion_giro'
            if dist_izq > dist_der:
                self.direccion_giro = self.velocidad_angular
            else:
                self.direccion_giro = -self.velocidad_angular
            
            cmd.linear.x = 0.0
            cmd.angular.z = self.direccion_giro
            
        # CASO 4: CORRECCIONES LATERALES SUAVES (Solo si el frente está totalmente seguro)
        else:
            self.estado = 'avanzar'
            if dist_izq < self.distancia_minima:
                cmd.linear.x = self.velocidad_lineal * 0.5  # Al corregir, frena un poco
                cmd.angular.z = -0.35                       # Gira a la derecha
                self.estado = 'corrigiendo derecha'
            elif dist_der < self.distancia_minima:
                cmd.linear.x = self.velocidad_lineal * 0.5  # Al corregir, frena un poco
                cmd.angular.z = 0.35                       # Gira a la izquierda
                self.estado = 'corrigiendo izquierda'
            else:
                # Camino 100% libre
                cmd.linear.x = self.velocidad_lineal
                cmd.angular.z = 0.0
        
        # Imprimir logs informativos del estado actual
        self.get_logger().info(f'Estado: {self.estado.upper()} | C: {dist_centro:.2f}m | I: {dist_izq:.2f}m | D: {dist_der:.2f}m')
        self.pub.publish(cmd)

def main():
    rclpy.init()
    node = EvasionObstaculosAvanzada()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
