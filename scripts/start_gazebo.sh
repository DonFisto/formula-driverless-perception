#!/usr/bin/env bash

# Stop on error
set -e

echo "=== Starting Gazebo with ROS 2 Humble ==="

# 1. Source ROS 2
source /opt/ros/humble/setup.bash

# Optional: source workspace if you have robot descriptions or plugins there
source ~/gazebo_ws/install/setup.bash

# 2. Launch Gazebo 
ros2 launch fs_basic_robot sim.launch.py 

