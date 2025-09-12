#!/usr/bin/env bash
# Quick environment sanity check

echo "Python: $(python3 --version)"
echo "ROS 2: $(ros2 --version 2>/dev/null || echo 'not found')"

echo "Checking CARLA module..."
python3 - <<'PY'
try:
    import carla
    print("CARLA module path:", carla.__file__)
except Exception as e:
    print("CARLA not available:", e)
PY

echo "Checking ROS topics..."
ros2 topic list 2>/dev/null | grep carla || echo "No CARLA topics yet (start bridge + spawner)"
