# FinalExam ROS — Hướng Dẫn Sử Dụng

Package điều khiển robot 4 bánh Mecanum + ARM trong môi trường Gazebo (ROS 2 Humble).

---

#### Cấu Trúc Package

```
finalexam_ros/
├── urdf/           # Mô hình robot (final.urdf)
├── config/         # Cấu hình controller (controllers.yaml)
├── launch/         # File khởi động (gazebo.launch.py)
```

---

## Hướng Dẫn Khởi Động
### Bước 0: Gitclone
```bash
# Tạo thư mục workspace nếu chưa có
mkdir -p ~/ros2_ws/
cd ~/ros2_ws/

# Clone dự án (Lệnh này tự động tạo thư mục finalexam_ros bên trong src)
git clone git clone https://github.com/ductoris/ros2_finalexam.git 
```

Cấu trúc thư mục chuẩn nhất:
```
[tên ws của bạn]/
├── src/           
  ├── finalexam_ros/        
          ├── urdf/         
```

### Bước 1 — Build package
#### QUAN TRỌNG:
```bash
Bạn mở file: src/finalexam_ros/urdf/final.urdf
Kéo xuống dòng: 402, sửa theo đúng đường dẫn trỏ đến .../src/finalexam_ros/config/controllers.yaml
Sau đó mới thực hiện bước tiếp theo
```

```bash
cd ~/ro2_ws
colcon build --packages-select finalexam_ros
source install/setup.bash
```

### Bước 2 — Khởi động Gazebo (Terminal 1)

```bash
ros2 launch finalexam_ros gazebo.launch.py
```

> Chờ Gazebo load xong (~12 giây) trước khi mở các terminal tiếp theo.

---

## Điều Khiển Robot
```bash
sudo apt update && sudo apt install -y \
  ros-humble-gazebo-ros2-control \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-teleop-twist-keyboard
```
### Terminal 2 — Điều Khiển ARM

**Cách 1:** Gửi lệnh trực tiếp (1 lần)

```bash
ros2 topic pub --once /arm_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.07, 1.0]}"
```

**Cách 2:** Điều khiển tăng dần (khuyến nghị)

```bash
ros2 run finalexam_ros arm_incremental_teleop
```

---

### Terminal 3 — Điều Khiển Bánh Xe (Mecanum Drive)

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r /cmd_vel:=/mecanum_drive_controller/reference_unstamped
```

#### Bảng phím điều khiển

| Hành Động       | Phím thường | Phím + Shift |
|-----------------|:-----------:|:------------:|
| Tiến            | `i`         | `I`          |
| Lùi             | `,`         | `<`          |
| Xoay Trái       | `j`         | —            |
| Xoay Phải       | `l`         | —            |
| Đi Ngang Trái   | —           | `J`          |
| Đi Ngang Phải   | —           | `L`          |
| Dừng lại        | `k`         | `K`          |

> **Tip:** Giữ `Shift` để kích hoạt chế độ đi ngang — đặc trưng của bánh Mecanum!

---

## Theo Dõi Dữ Liệu

### Terminal 4 — Hiển Thị Encoder (Joint States)

```bash
ros2 topic echo /joint_states
```

### Terminal 5 — Hiển Thị IMU

```bash
ros2 topic echo /imu
```

---

## Tổng Hợp — Mở 5 Terminal

| Terminal | Lệnh | Mục đích |
|----------|------|----------|
| 1 | `ros2 launch finalexam_ros gazebo.launch.py` | Khởi động môi trường |
| 2 | `ros2 run finalexam_ros arm_incremental_teleop` | Điều khiển ARM |
| 3 | `ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/mecanum_drive_controller/reference_unstamped` | Điều khiển bánh xe |
| 4 | `ros2 topic echo /joint_states` | Xem Encoder |
| 5 | `ros2 topic echo /imu` | Xem IMU |

---

##  Thông Số Kỹ Thuật Robot

| Thông số | Giá trị |
|----------|---------|
| Loại bánh | Mecanum (4 bánh omni) |
| Bán kính bánh | 0.05 m |
| Khoảng cách trục X | 0.30 m |
| Khoảng cách trục Y | 0.24 m |
| Tốc độ tối đa | 1.0 m/s (tịnh tiến), 2.0 rad/s (quay) |

---

##  Troubleshooting

**Gazebo không spawn robot:**
```bash
# Đợi đủ thời gian load (~15 giây) rồi kiểm tra
ros2 topic list | grep robot_description
```

**Controller không load được:**
```bash
ros2 control list_controllers
```

**Không nhận lệnh điều khiển:**
```bash
# Kiểm tra topic có đang publish không
ros2 topic echo /mecanum_drive_controller/reference_unstamped
```


