from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'finalexam_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Launch files
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.py'))),  # SỬA: pattern đơn giản hơn, chắc chắn lấy đủ

        # URDF files
        (os.path.join('share', package_name, 'urdf'),
            glob(os.path.join('urdf', '*.urdf'))),  # SỬA: chỉ lấy .urdf, tránh lấy nhầm file khác
        
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        # Meshes — SỬA: thêm recursive để lấy file trong subfolder nếu có
        (os.path.join('share', package_name, 'meshes'),
            glob(os.path.join('meshes', '*.STL')) +
            glob(os.path.join('meshes', '*.dae'))),
        (os.path.join('share', package_name, 'config'),
        glob(os.path.join('config', '*.yaml'))),
        (os.path.join('lib', package_name), ['finalexam_ros/arm_incremental_teleop.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ductri',
    maintainer_email='ductri@todo.todo',
    description='Mô phỏng robot mdt6 trong Gazebo',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'keyboard_teleop = finalexam_ros.keyboard_teleop:main',
        'imu_reader = finalexam_ros.imu_reader:main',
        'arm_incremental_teleop = finalexam_ros.arm_incremental_teleop:main',
    ],
},
)
