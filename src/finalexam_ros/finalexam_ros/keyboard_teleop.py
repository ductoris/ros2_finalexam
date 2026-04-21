#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist  # Đổi từ TwistStamped sang Twist
import sys, tty, termios

LIN = 1.0  # Tăng tốc độ lên một chút để dễ thấy xe chạy
ANG = 1.5

MOVES = {
    'w': (LIN,  0.0, 0.0),   # tiến
    's': (-LIN, 0.0, 0.0),   # lùi
    'a': (0.0,  0.0, ANG),   # quay trái
    'd': (0.0,  0.0, -ANG),  # quay phải
    'q': (0.0,  LIN, 0.0),   # trượt trái (Y dương)
    'e': (0.0, -LIN, 0.0),   # trượt phải (Y âm)
    ' ': (0.0,  0.0, 0.0),   # dừng
}

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return key

class Teleop(Node):
    def __init__(self):
        super().__init__('teleop_mecanum')
        # Sửa lại topic và kiểu msg
        self.pub = self.create_publisher(
            Twist, 
            '/mecanum_drive_controller/cmd_vel_unstamped', 
            10
        )

    def send(self, vx, vy, wz):
        msg = Twist()
        msg.linear.x = vx
        msg.linear.y = vy
        msg.angular.z = wz
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = Teleop()

    print("""
==== MECANUM TELEOP CHUẨN ====
W/S   : TIẾN / LÙI
Q/E   : TRƯỢT TRÁI / PHẢI (MECANUM)
A/D   : QUAY TRÁI / QUAY PHẢI
SPACE : DỪNG KHẨN CẤP
X     : THOÁT
==============================
""")

    try:
        while rclpy.ok():
            key = get_key().lower()
            if key == 'x':
                break
            if key in MOVES:
                v_x, v_y, a_z = MOVES[key]
                node.send(v_x, v_y, a_z)
            else:
                node.send(0.0, 0.0, 0.0)
    except Exception as e:
        print(e)
    finally:
        node.send(0.0, 0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()