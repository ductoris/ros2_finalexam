import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import math

class ImuSensingNode(Node):
    def __init__(self):
        super().__init__('imu_reader_node')
        
        # Subscribe vào đúng topic bạn đang có
        self.subscription = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10)
        
        self.get_logger().info('Đã bắt đầu nhận dữ liệu từ IMU...')

    def imu_callback(self, msg):
        # 1. Lấy dữ liệu Orientation (Quaternion)
        qx = msg.orientation.x
        qy = msg.orientation.y
        qz = msg.orientation.z
        qw = msg.orientation.w

        # 2. Chuyển đổi Quaternion sang Euler (Pitch, Roll, Yaw) để dễ đọc
        siny_cosp = 2 * (qw * qz + qx * qy)
        cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        # Đổi sang độ cho dễ quan sát
        yaw_deg = math.degrees(yaw)

        # 3. Lấy dữ liệu Gia tốc (Linear Acceleration)
        acc_x = msg.linear_acceleration.x
        acc_y = msg.linear_acceleration.y
        acc_z = msg.linear_acceleration.z

        # In dữ liệu ra màn hình
        self.get_logger().info(f'\n--- IMU DATA ---\nHướng (Yaw): {yaw_deg:.2f}°\nGia tốc Z: {acc_z:.2f} m/s²')

def main(args=None):
    rclpy.init(args=args)
    node = ImuSensingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()