# Environment Setup

## 1. System Requirements
- Supported OS: Ubuntu 22.04 (Humble-Carla_0.9.15) / Ubuntu 20.04 (Foxy-Carla_0.9.13)
- GPU: NVIDIA with drivers + CUDA
- ROS2 distribution: Humble (Carla_0.9.15) / Foxy (Carla_0.9.13)

## 2. Installing CARLA simulator
- Download CARLA release (0.9.15/0.9.13) from official GitHub 
- Extract to a chosen directory
- Run simulator: ./CarlaUE4.sh 

## 3. Installing Ros-Bridge
- Create a colcon workspace
	`mkdir -p ~/carla-ros-bridge/src`
	`cd ~/carla-ros-bridge/src`
- Clone the official repositories 
	`git clone https://github.com/carla-simulator/ros-bridge.git`
	`git clone https://github.com/carla-simulator/ros-carla-msgs.git`
- Compile the bridge
	`sudo apt update`
	`sudo apt install -y python3-pip python3-colcon-common-extensions ros-${ROS_DISTRO}-pcl-conversions`
	`pip3 install transforms3d`
	`cd ~/carla-ros-bridge`
	`colcon build --symlink-install`
- Execute the bridge
	`cd ~/carla-ros-bridge`
	`ros2 launch carla_ros_bridge carla_ros_bridge_with_example_ego_vehicle.launch.py`