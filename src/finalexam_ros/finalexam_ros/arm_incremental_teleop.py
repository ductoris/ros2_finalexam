import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import sys, select, termios, tty
import math

msg = """
Điều khiển tay máy Incremental - Mai Đức Trí
--------------------------------------------
Khớp 2 (Xoay):
    1 / ! : +10 độ / -10 độ
    2 / @ : +20 độ / -20 độ
    5 / % : +5 độ  / -5 độ

Khớp 1 (Tịnh tiến):
    . (dấu chấm) : Nâng lên +0.05m
    , (dấu phẩy) : Hạ xuống -0.05m

Phím khác:
    R : Reset về [0, 0]
    CTRL-C để thoát
--------------------------------------------
"""

class ArmTeleop(Node):
    def __init__(self):
        super().__init__('arm_incremental_teleop')
        self.pub = self.create_publisher(Float64MultiArray, '/arm_controller/commands', 10)
        
        # Trạng thái hiện tại của khớp [Joint1, Joint2]
        self.current_pos = [0.0, 0.0]
        
        # Giới hạn của robot (Theo URDF của bạn)
        self.j1_min, self.j1_max = -0.11, 0.0
        self.j2_min, self.j2_max = 0.0, 2.0933 # ~120 độ

    def send_cmd(self):
        # Đảm bảo giá trị không vượt quá giới hạn vật lý
        self.current_pos[0] = max(min(self.current_pos[0], self.j1_max), self.j1_min)
        self.current_pos[1] = max(min(self.current_pos[1], self.j2_max), self.j2_min)
        
        command = Float64MultiArray()
        command.data = self.current_pos
        self.pub.publish(command)
        print(f"Vị trí hiện tại: Joint1(L)= {self.current_pos[0]:.3f}m | Joint2(R)= {math.degrees(self.current_pos[1]):.1f}°")

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    arm_node = ArmTeleop()

    deg10 = math.radians(10)
    deg20 = math.radians(20)
    deg5  = math.radians(5)

    try:
        print(msg)
        while True:
            key = get_key(settings)
            
            # --- Khớp 2 (Xoay) ---
            if key == '1': arm_node.current_pos[1] += deg10
            elif key == '!': arm_node.current_pos[1] -= deg10
            elif key == '2': arm_node.current_pos[1] += deg20
            elif key == '@': arm_node.current_pos[1] -= deg20
            elif key == '5': arm_node.current_pos[1] += deg5
            elif key == '%': arm_node.current_pos[1] -= deg5
            
            # --- Khớp 1 (Tịnh tiến) ---
            elif key == '.': arm_node.current_pos[0] += 0.01
            elif key == ',': arm_node.current_pos[0] -= 0.01
            
            # --- Reset ---
            elif key.lower() == 'r':
                arm_node.current_pos = [0.0, 0.0]
                
            elif key == '\x03': break # Ctrl+C
            
            arm_node.send_cmd()
            
    except Exception as e:
        print(e)
    finally:
        rclpy.shutdown()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == '__main__':
    main()