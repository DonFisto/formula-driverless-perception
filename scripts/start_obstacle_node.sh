#!/usr/bin/env bash

# Stop on error
set -e

echo "=== Starting LiDAR obstacle detection node ==="

# 1. Source ROS 2
source /opt/ros/humble/setup.bash

# 2. Source perception workspace
source ~/perception_ws/install/setup.bash

# 3. Run obstacle detection node
ros2 run lidar_perception obstacle_node

