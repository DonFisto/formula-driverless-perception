#!/usr/bin/env bash
# Spawn ego vehicle with sensors

source /opt/ros/humble/setup.bash
source ~/carla-ros-bridge/install/setup.bash

ros2 run carla_spawn_objects carla_spawn_objects   --ros-args   -p objects_definition_file:=$(ros2 pkg prefix carla_spawn_objects)/share/carla_spawn_objects/config/objects.json   -p spawn_point:='0,0,0,0,0,0'
