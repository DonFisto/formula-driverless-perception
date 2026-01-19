#!/usr/bin/env bash
# Start CARLA Simulator
cd ~/CARLA_0.9.15 || exit 1
./CarlaUE4.sh -carla-world-port=2000 -quality-level=Low

