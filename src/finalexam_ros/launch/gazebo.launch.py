import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (ExecuteProcess, DeclareLaunchArgument, 
                             TimerAction, SetEnvironmentVariable)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'finalexam_ros'
    pkg_share = get_package_share_directory(package_name)

    # ĐỊNH NGHĨA ĐƯỜNG DẪN RVIZ (Bạn thiếu dòng này nên bị báo lỗi)
    rviz_config_path = os.path.join(pkg_share, 'config', 'view_robot.rviz')
    controller_config = os.path.join(pkg_share, 'config', 'controllers.yaml')
    # Thiết lập đường dẫn Model cho Gazebo
    gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=os.path.join(pkg_share, '..') + ':' +
              os.environ.get('GAZEBO_MODEL_PATH', '')
    )

    # Đọc file URDF
    urdf_path = os.path.join(pkg_share, 'urdf', 'final.urdf')
    with open(urdf_path, 'r') as f:
        robot_desc = f.read()

    world_path = os.path.join(pkg_share, 'worlds', 'my_map.world')
    world_file_arg = DeclareLaunchArgument(
        'world',
        default_value=world_path,
        description='Full path to world file'
    )

    return LaunchDescription([
        gazebo_model_path,
        world_file_arg,
        Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                parameters=[{'robot_description': robot_desc, 'use_sim_time': True}],
                output='screen'
            ),
        # 1. Chạy Gazebo Server
        ExecuteProcess(
            cmd=['gzserver', '--verbose', LaunchConfiguration('world'),
                 '-s', 'libgazebo_ros_init.so',
                 '-s', 'libgazebo_ros_factory.so',
                 '--ros-args', '--params-file', controller_config],
            output='screen'
        ),

        # 2. Chạy Gazebo Client
        ExecuteProcess(cmd=['gzclient'], output='screen'),

        # 3. Nạp Robot State Publisher & RViz & Spawn (Sau 5s)
        TimerAction(period=5.0, actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=['-entity', 'finalexam_ros', '-topic', 'robot_description', '-z', '0.3'],
                output='screen'
            ),
            Node(
                package='rviz2',
                executable='rviz2',
                arguments=['-d', rviz_config_path],
                parameters=[{'use_sim_time': True}],
                output='screen'
            )
        ]),

        # 4. Joint State Broadcaster (Đây chính là ENCODER)
        TimerAction(period=8.0, actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
                output='screen'
            ),
        ]),

        # 5. Các Controller khác
        TimerAction(period=10.0, actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['mecanum_drive_controller', '--controller-manager', '/controller_manager'],
                output='screen'
            ),
        ]),
        TimerAction(period=12.0, actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['arm_controller', '--controller-manager', '/controller_manager'],
                output='screen'
            ),
        ]),
    ])