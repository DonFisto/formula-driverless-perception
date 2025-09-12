#!/usr/bin/env bash
# Start CARLA ROS 2 Bridge

# clean Python env
conda deactivate 2>/dev/null || true
unset PYTHONPATH

# source ROS 2 and bridge
source /opt/ros/humble/setup.bash
source ~/carla-ros-bridge/install/setup.bash

# use CycloneDDS
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

ros2 launch carla_ros_bridge carla_ros_bridge.launch.py
