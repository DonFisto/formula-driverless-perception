#!/bin/bash

SESSION=flexirover

tmux kill-session -t "$SESSION" 2>/dev/null

tmux new-session -d -s "$SESSION" -n "gazebo"

# 0 — Gazebo world
tmux send-keys -t "$SESSION:0" "
source /opt/ros/jazzy/setup.zsh
source ~/gazebo_ws/install/setup.zsh

gz sim -r ~/gazebo_ws/src/fs_robot_description_jazzy/worlds/flexirover_world.sdf
" C-m

sleep 4

# 1 — Spawn FlexiRover
tmux new-window -t "$SESSION:1" -n "spawn"
tmux send-keys -t "$SESSION:1" "
source /opt/ros/jazzy/setup.zsh
source ~/gazebo_ws/install/setup.zsh

ros2 run ros_gz_sim create \
-file ~/gazebo_ws/src/fs_robot_description_jazzy/models/flexirover/model.sdf \
-name flexirover \
-x 0 -y 0 -z 0
" C-m

sleep 2

# 2 — LiDAR bridge
tmux new-window -t "$SESSION:2" -n "scan_bridge"
tmux send-keys -t "$SESSION:2" "
source /opt/ros/jazzy/setup.zsh

ros2 run ros_gz_bridge parameter_bridge \
/flexirover/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan
" C-m

sleep 1

# 3 — cmd_vel bridge
tmux new-window -t "$SESSION:3" -n "cmd_bridge"
tmux send-keys -t "$SESSION:3" "
source /opt/ros/jazzy/setup.zsh

ros2 run ros_gz_bridge parameter_bridge \
/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
" C-m

sleep 1

# 4 — Static TF
tmux new-window -t "$SESSION:4" -n "tf"
tmux send-keys -t "$SESSION:4" "
source /opt/ros/jazzy/setup.zsh

ros2 run tf2_ros static_transform_publisher \
0 0 0 0 0 0 \
world flexirover/base_link/lidar
" C-m

sleep 1

# 5 — Scan to PointCloud2
tmux new-window -t "$SESSION:5" -n "cloud"
tmux send-keys -t "$SESSION:5" "
source /opt/ros/jazzy/setup.zsh
source ~/perception_ws/install/setup.zsh

ros2 run lidar_perception scan_to_cloud_node
" C-m

sleep 1

# 6 — Obstacle perception
tmux new-window -t "$SESSION:6" -n "obstacles"
tmux send-keys -t "$SESSION:6" "
source /opt/ros/jazzy/setup.zsh
source ~/perception_ws/install/setup.zsh

ros2 run lidar_perception obstacle_node
" C-m

sleep 1

# 7 — Local occupancy grid
tmux new-window -t "$SESSION:7" -n "occupancy"
tmux send-keys -t "$SESSION:7" "
source /opt/ros/jazzy/setup.zsh
source ~/perception_ws/install/setup.zsh

ros2 run lidar_perception occupancy_grid_node
" C-m

sleep 1

# 8 — Reactive navigation
tmux new-window -t "$SESSION:8" -n "reactive_nav"
tmux send-keys -t "$SESSION:8" "
source /opt/ros/jazzy/setup.zsh
source ~/perception_ws/install/setup.zsh

ros2 run lidar_perception reactive_navigation_node
" C-m

sleep 1

# 9 — RViz
tmux new-window -t "$SESSION:9" -n "rviz"
tmux send-keys -t "$SESSION:9" "
source /opt/ros/jazzy/setup.zsh
source ~/perception_ws/install/setup.zsh

rviz2
" C-m

tmux select-window -t "$SESSION:0"
tmux attach-session -t "$SESSION"
