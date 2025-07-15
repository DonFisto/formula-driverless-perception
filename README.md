# 🏎️ Formula Student Driverless - Perception Stack

This project is a modular perception system for a simulated Formula Student Driverless car. It integrates real-time camera and LiDAR perception, object detection with YOLOv5, and SLAM for localization — all using ROS 2.

> 💡 **Goal**: Prepare to contribute to a real FS Driverless team by building a perception pipeline from scratch using simulation and open-source tools.

---

## Features

- ROS2-based modular architecture
- Real-time camera integration via `cv_camera`
- Object detection using YOLOv5 + PyTorch
- LiDAR data processing and visualization
- SLAM with `slam_toolbox` or `cartographer_ros`
- TF2 and coordinate transform handling
- Rviz visualization for debugging and analysis

---

## Project Structure

```bash
fs_perception/
├── src/                     # ROS2 packages
│   ├── camera_node/
│   ├── yolo_detection/
│   ├── lidar_processing/
│   └── slam/
├── launch/                  # Unified launch files
├── scripts/                 # Utility scripts (e.g. setup, playback)
├── docs/                    # Architecture diagrams, notes, and roadmap
└── README.md
```

---

## Quick Start

> Recommended: ROS 2 Foxy or Humble, Ubuntu 20.04+

```bash
# Clone the repo
git clone https://github.com/yourusername/fs_perception.git
cd fs_perception

# Build the workspace
colcon build

# Source it
source install/setup.bash

# Launch camera + YOLO detection
ros2 launch launch/camera_yolo.launch.py
```

---

## Learning Roadmap

This repo follows a structured learning path:
- Week 1: ROS2 basics & project setup
- Week 2–3: Camera + YOLOv5 integration
- Week 4: LiDAR data capture & filtering
- Week 5: SLAM and map building
- Week 6: Full integration & testing

See [`docs/roadmap.md`](docs/roadmap.md) for detailed progress.

---

## Screenshots & Diagrams

*(To be added later)*  
- [ ] Sample YOLO detections  
- [ ] SLAM map in RViz  
- [ ] System architecture diagram

---

## Resources & References

- [ROS2 Documentation](https://docs.ros.org/)
- [YOLOv5 GitHub](https://github.com/ultralytics/yolov5)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)

---

## Contributions

This is a solo learning project, but feel free to open issues or forks if you're interested in this stack!

---

## Author
Daniel Martínez-Cabeza de Vaca Guillén 
Dual Degree in Mathematics & Computer Science  
Universidad de Murcia
