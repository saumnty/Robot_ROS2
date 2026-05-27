import socket
import json
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ServidorControl(Node):
    def __init__(self):
        super().__init__('servidor_matlab')
        self.pub = self.create_publisher(Twist, '/model/bolitabot/cmd_vel', 10)
        self.get_logger().info('Servidor listo, esperando comandos de MATLAB...')

    def publicar(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)
        self.pub.publish(msg)

def main():
    rclpy.init()
    nodo = ServidorControl()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('0.0.0.0', 9090))
    servidor.listen(5)
    print('Escuchando en puerto 9090...')

    while True:
        conn, addr = servidor.accept()
        print(f'Conexion de {addr}')
        data = conn.recv(1024).decode()
        try:
            cmd = json.loads(data)
            nodo.publicar(cmd.get('linear_x', 0.0), cmd.get('angular_z', 0.0))
            conn.send(b'OK')
            print(f'Comando enviado: linear={cmd.get("linear_x")}, angular={cmd.get("angular_z")}')
        except Exception as e:
            conn.send(f'ERROR: {e}'.encode())
        conn.close()
        rclpy.spin_once(nodo, timeout_sec=0.1)

if __name__ == '__main__':
    main()
