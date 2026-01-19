#!/usr/bin/env bash
# Spawn ego vehicle with sensors

conda deactivate 2>/dev/null || true
unset PYTHONPATH
source ~/carla-venv/bin/activate
source /opt/ros/humble/setup.bash
source ~/carla-ros-bridge/install/setup.bash

ros2 launch carla_spawn_objects carla_spawn_objects.launch.py \
  objects_definition_file:=/home/$USER/carla-ros-bridge/config/ego_minimal.json
