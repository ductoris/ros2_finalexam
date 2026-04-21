from launch import LaunchDescription
from launch_ros.actions import Node
import os

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Lấy đường dẫn package
    pkg_path = get_package_share_directory('finalexam_ros')

    # Đường dẫn tới file URDF
    urdf_file = os.path.join(pkg_path, 'urdf', 'final.urdf')

    # 🔥 Đọc trực tiếp URDF (cách chắc chắn nhất)
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([

        # Publish robot_description + TF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}],
            output='screen'
        ),

        # GUI điều khiển joint
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen'
        ),

        # RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        )
    ])
