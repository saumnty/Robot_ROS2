import socket
import json
import rclpy
import math
import threading
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class ServidorControl(Node):
    def __init__(self):
        super().__init__('servidor_matlab')
        # Publicar la velocidad
        self.pub = self.create_publisher(Twist, '/model/bolitabot/cmd_vel', 10)
        self.get_logger().info('Servidor listo, esperando comandos de MATLAB...')
        # Suscribirse a la odometría
        self.sub = self.create_subscription(Odometry, '/model/bolitabot/odometry', self.cb_odom, 10)
        self.get_logger().info('Suscrito a /model/bolitabot/odometry')

        # variables actuales
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.get_logger().info('Servidor Full-Duplex listo')

    def cb_odom(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        # Convertir quaternion a ángulo (yaw)
        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.theta = math.atan2(siny_cosp, cosy_cosp)
    
    def publicar(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)
        self.pub.publish(msg)

def ros_spin(nodo):
    # Esto mantiene a ROS escuchando la odometría en segundo plano
    rclpy.spin(nodo)

def main():
    rclpy.init()
    nodo = ServidorControl()

    # Iniciamos ROS en un hilo separado
    hilo_ros = threading.Thread(target=ros_spin, args=(nodo,))
    hilo_ros.start()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('0.0.0.0', 9090))
    servidor.listen(5)
    print('Escuchando en puerto 9090...')

    try:
        while True:
            conn, addr = servidor.accept() # Esperar a que un cliente se conecte
            print(f'Conexion de {addr}')
            data = conn.recv(1024).decode() # Recibir el comando del cliente
            if data:
                try:
                    cmd = json.loads(data) # Esperamos un JSON con 'linear_x' y 'angular_z'
                    nodo.publicar(cmd.get('linear_x', 0.0), cmd.get('angular_z', 0.0))

                    estado = {"x": nodo.x, "y": nodo.y, "theta": nodo.theta}
                    conn.send(json.dumps(estado).encode())

                except Exception as e:
                    conn.send(f'{{"error": "{e}"}}'.encode())

            conn.close() # Cerrar la conexión con el cliente
    
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown() # Detener ROS
        servidor.close() # Cerrar el socket

if __name__ == '__main__':
    main()
