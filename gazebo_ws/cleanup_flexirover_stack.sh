#!/bin/bash

tmux kill-session -t flexirover 2>/dev/null

pkill -9 -f "gz sim" 2>/dev/null
pkill -9 -f "ros_gz_bridge" 2>/dev/null
pkill -9 -f "rviz2" 2>/dev/null
pkill -9 -f "scan_to_cloud_node" 2>/dev/null
pkill -9 -f "obstacle_node" 2>/dev/null
pkill -9 -f "occupancy_grid_node" 2>/dev/null
pkill -9 -f "reactive_navigation_node" 2>/dev/null
pkill -9 -f "static_transform_publisher" 2>/dev/null

echo "FlexiRover stack cleaned."
