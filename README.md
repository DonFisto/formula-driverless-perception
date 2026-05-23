# 🏎️ Formula Student Driverless - LiDAR Perception and Reactive Navigation

This project develops a **modular LiDAR-based perception and reactive navigation pipeline** for a simulated autonomous vehicle using **ROS 2 Humble** and **Gazebo Classic**.

> 💡 **Goal**: Build and understand a lightweight autonomous driving stack from scratch, aligned with the type of modular architectures used in Formula Student Driverless teams.

---

## Current Scope

The project focuses on a **reduced but realistic autonomy pipeline** that can be completed and demonstrated reliably within the available timeframe.

### Main Objective
Develop a working pipeline for:

- LiDAR-based obstacle detection
- Obstacle representation using bounding boxes
- Reactive obstacle avoidance
- RViz visualization and reproducible ROS 2 integration

### Current Pipeline

Perception → Reactive Navigation

The robot should:

1. Detect obstacles using LiDAR  
2. Cluster point cloud data  
3. Represent obstacles with AABB / OBB boxes  
4. Publish structured obstacle information  
5. Move autonomously in simulation while avoiding collisions  

---

## Why This Scope

The project originally started with **CARLA + ROS Bridge**, aiming to cover perception, localization, planning, and control.

However, due to:

- High RAM usage  
- Instability on mid-range hardware  
- Simulator complexity relative to the available timeframe  

the project was **re-scoped and migrated to Gazebo Classic**.

This allows the project to remain:

- Technically solid  
- Reproducible  
- Focused on robotics fundamentals  
- Feasible within the current deadline  

---

## Features

### Implemented / In Progress

- ROS 2 Humble modular architecture  
- Gazebo Classic simulation environment  
- LiDAR perception using `PointCloud2`  
- Point cloud clustering with **DBSCAN**  
- **AABB (Axis-Aligned Bounding Boxes)**  
- **OBB (Oriented Bounding Boxes)**  
- RViz visualization of LiDAR and detected obstacles  
- Voxel downsampling for perception stabilization  

### Planned in the Current Scope

- EMA temporal smoothing for obstacle stability  
- Structured obstacle publishing  
- Reactive navigation node  
- Obstacle-aware motion in Gazebo  
- Launch files and reproducible demo workflow  

---

## Project Structure
```
project_root/
│
├── gazebo_ws/                 # Gazebo / robot simulation workspace
│   ├── src/
│   ├── build/
│   ├── install/
│   └── log/
│
├── perception_ws/             # LiDAR perception workspace
│   ├── src/
│   │   └── lidar_perception/
│   ├── build/
│   ├── install/
│   └── log/
│
├── docs/                      # Notes, setup, timeline, architecture
├── scripts/                   # Utility scripts for launching environment
└── README.md
```
---

## Tech Stack

- Ubuntu 22.04  
- ROS 2 Humble  
- Gazebo Classic  
- Python 3.10  
- RViz2  
- NumPy  
- scikit-learn (DBSCAN)

---

## Quick Start

### 1. Source ROS2

source /opt/ros/humble/setup.bash

### 2. Launch Gazebo

ros2 launch gazebo_ros gazebo.launch.py \
world:=/opt/ros/humble/share/gazebo_ros/worlds/empty.world

### 3. Build and Source the Perception Workspace

cd ~/perception_ws  
colcon build --symlink-install  
source install/setup.bash

### 4. Run the Obstacle Detection Node

ros2 run lidar_perception obstacle_node

### 5. Visualize in RViz2

rviz2

Typical RViz displays:

- PointCloud2 → raw LiDAR  
- MarkerArray → detected obstacles  
- TF → robot frame tree  

---

## Development Roadmap (Current 3-Week Plan)

The project follows a **3-week (24 hour) execution plan**.

### Week 1 — Perception Stabilization

- Refactor and clean perception node  
- Add voxel downsampling  
- Tune DBSCAN parameters  
- Add EMA temporal smoothing  
- Publish structured obstacle data  

### Week 2 — Reactive Navigation

- Create navigation node  
- Evaluate nearest obstacles  
- Implement steering logic  
- Tune motion parameters  
- Test in multiple scenarios  

### Week 3 — Polish and Delivery

- Refactor and clean codebase  
- Create launch files  
- Record demo video  
- Write technical documentation  
- Prepare presentation slides  

---

## Out of Scope (Current Version)

To keep the project realistic and finishable, the following are **not part of the current deliverable**:

- CARLA integration  
- Camera perception  
- YOLO / deep learning object detection  
- SLAM  
- Global path planning  
- Pure Pursuit / Stanley controllers  
- Multi-sensor fusion  
- Real vehicle deployment  

These remain possible **future extensions**.

---

## Current Status

The project currently includes:

- Stable Gazebo simulation  
- Functional LiDAR data acquisition  
- Obstacle clustering using DBSCAN  
- AABB bounding boxes  
- OBB bounding boxes  
- RViz visualization of perception results  

This places the project in an **advanced perception stage**, ready to integrate reactive navigation.

---

## Documentation

Documentation is stored in the `docs/` directory.

Recommended documents:

- docs/environment_setup.md  
- docs/timeline.md  
- docs/perception_notes.md  

These files track setup instructions, development progress, and architectural notes.

---

## Future Work

Possible extensions after completing the current scope:

- Temporal filtering with obstacle tracking  
- Velocity estimation of obstacles  
- SLAM integration  
- Global planning algorithms  
- Advanced control strategies  
- Migration to richer simulators  
- Real hardware deployment  
- Formula Student-specific cone detection and track navigation  

---

## License

This project is released under the **MIT License**.

---

## Author

Daniel Martínez-Cabeza de Vaca Guillén  
Dual Degree in Mathematics & Computer Science  
Universidad de Murcia
