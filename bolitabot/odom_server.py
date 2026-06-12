import json
import math
import threading
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

ODOM_FILE = '/root/mis_robots/bolitabot/odom_data.json'

class OdomServer(Node):
    def __init__(self):
        super().__init__('odom_server')
        self.create_subscription(Odometry, '/model/bolitabot/odometry', self.cb, 10)
        self.get_logger().info('OdomServer listo - escribiendo en archivo')

    def cb(self, msg):
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        data = {
            'x': msg.pose.pose.position.x,
            'y': msg.pose.pose.position.y,
            'theta': 2.0 * math.atan2(qz, qw)
        }
        with open(ODOM_FILE, 'w') as f:
            json.dump(data, f)

def main():
    rclpy.init()
    nodo = OdomServer()
    print('Escribiendo odometria en', ODOM_FILE)
    rclpy.spin(nodo)

if __name__ == '__main__':
    main()
