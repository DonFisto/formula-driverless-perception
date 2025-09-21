# Environment Setup

## 1. System Requirements
- Supported OS: Ubuntu 22.04 (Humble-Carla_0.9.15) / Ubuntu 20.04 (Foxy-Carla_0.9.13)
- GPU: NVIDIA with drivers + CUDA
- ROS2 distribution: Humble (Carla_0.9.15) / Foxy (Carla_0.9.13)

## 2. Installing CARLA simulator
- Download CARLA release (0.9.15/0.9.13) from official GitHub 
- Extract to a chosen directory
- Run simulator: ./CarlaUE4.sh 

## 3. Installing Ros-Bridge
- Create a colcon workspace
	mkdir -p ~/carla-ros-bridge/src
	cd ~/carla-ros-bridge/src
- Clone the official repositories 
	git clone https://github.com/carla-simulator/ros-bridge.git
	git clone https://github.com/carla-simulator/ros-carla-msgs.git
- Compile the bridge
	sudo apt update
	sudo apt install -y python3-pip python3-colcon-common-extensions ros-${ROS_DISTRO}-pcl-conversions
	pip3 install transforms3d
	cd ~/carla-ros-bridge
	colcon build --symlink-install
- Execute the bridge
	cd ~/carla-ros-bridge
	ros2 launch carla_ros_bridge carla_ros_bridge_with_example_ego_vehicle.launch.py

# CARLA + ROS Bridge Setup Timeline

This section summarizes the sessions spent building a working CARLA + ROS bridge environment, grouped into logical sessions.  

---

## Session 1 — First build, `tf2_eigen` missing
- Built `pcl_recorder`; compile failed: `fatal error: tf2_eigen/tf2_eigen.h: No such file or directory`.
- Discovered header actually lives under Humble as `tf2_eigen/tf2_eigen/tf2_eigen.h`.
- Tried header include fixes; CMake had found `tf2_eigen` but include path/layout mismatch.

## Session 2 — Include path experiments
- Verified the real path via `dpkg -L ros-humble-tf2-eigen`.
- Switched include to the double-namespace header; build then warned it’s obsolete and suggested `tf2_eigen.hpp`.
- Decided to keep as-is since it compiled.

## Session 3 — Launching the bridge, missing CARLA module
- `ros2 launch carla_ros_bridge...` failed: `ModuleNotFoundError: No module named 'carla'`.
- Realized Python path to CARLA wasn’t set / version mismatched.

## Session 4 — Version mismatch 0.9.13 vs 0.9.15
- Bridge required CARLA 0.9.13; you had 0.9.15.
- Bridge exited with: “CARLA python module version 0.9.13 required. Found: 0.9.15” and a shutdown attribute error.

## Session 5 — Branch/tag confusion & rebuilding
- Tried to checkout `ros-bridge` tag `0.9.13`—it wasn’t present the way we first used the command.
- Multiple rebuilds; duplicate packages issue (same packages in several subfolders).
- Cleaned the workspace layout to avoid duplicate package names.

## Session 6 — Terminal setup & missing executables
- Clarified which terminals run what (A = CARLA, B = bridge, C = spawner/tools).
- Hit “no executable found” for spawn scripts; ensured `colcon build` + `source install/setup.bash`.

## Session 7 — Repo layout fixes & `carla_msgs`
- Noticed `carla_msgs` was empty—learned it’s a separate repo (`ros-carla-msgs`).
- Added it; then hit `rosidl`/`empy` issues.

## Session 8 — `em` vs `empy`, `catkin_pkg`, other ROS IDL errors
- `rosidl_adapter` failed: `ModuleNotFoundError: No module named 'em'` / `em.BUFFERED_OPT` / `catkin_pkg`.
- Installed the correct packages (`python3-empy`, `python3-catkin-pkg`) and removed/conflicts with the `em` module.
- Rebuilt until IDL errors cleared.

## Session 9 — CARLA runtime deps
- Running local CARLA hit `libomp.so.5` missing; installed the OpenMP runtime.
- Confirmed CARLA server could start locally.

## Session 10 — Spawning actors & JSON issues
- Bridge launched but spawner failed: “blueprint not found” and invalid spawnpoint.
- Your JSON had single quotes & a truncated line—fixed to valid JSON with double quotes and full spawn fields.
- Still saw “blueprint not found” from the bridge while the CARLA Python API showed blueprints existed (mismatch likely from bridge not actually connecting / wrong CARLA version).

## Session 11 — Env/path cleanup & rebuilds
- Cleared `build/ install/ log/`, re-sourced Humble, rebuilt.
- Verified `ros2 pkg executables` showed `carla_spawn_objects`.

## Session 12 — More version wrangling (0.9.13 wheel/egg)
- Wrestling with `carla` wheel/egg installs and Python versions (3.7 vs 3.10).
- Learned: CARLA’s Python wheel must match the Python minor version used by the process.
- Eggs aren’t editable folders; can’t append `__version__` inside.

## Session 13 — Docker attempt for bridge (ROS Foxy)
- Built a `foxy` bridge container; hit `em` vs `empy` conflicts during `colcon build`.
- Adjusted Dockerfile to install `python3-empy`/remove `em`; build progressed but some packages (rviz plugin, `pcl_recorder`) needed extra deps.

## Session 14 — Running CARLA in Docker
- Tried CARLA server container with `-opengl`/offscreen; container exited quickly; only “xdg-user-dir not found”.
- Switching to interactive showed Vulkan/Offscreen crashes (swapchain error), so containerized CARLA was unstable on your GPU/driver stack.

## Session 15 — Pivot: CARLA native + bridge in container
- Decided to run CARLA natively (works) and bridge inside container with `--network host`.
- Bridge then failed inside container: `No module named 'carla'` (container Python couldn’t import local CARLA; version mismatch again).
- Attempted to copy in a 3.7 wheel to Foxy (Python 3.8) container—wheel not supported.

## Session 16 — More build/image iterations
- Tried installing Python 3.7 inside Foxy image; packages unavailable from Ubuntu base.
- Reworked approach; still hitting “not a supported wheel” when wheel Python tag didn’t match container Python.

## Session 17 — Vulkan/OpenGL diagnostics
- Verified NVIDIA container toolkit works (`nvidia-smi` in container good).
- Confirmed Vulkan in CARLA container still crashes; concluded: run CARLA locally and keep bridge in a container.

## Session 18 — Return to 0.9.15 (everything aligned)
- Installed CARLA 0.9.15 and `ros-bridge` matching it; builds fine on host (Humble).
- Ran the example launch successfully; blueprints/TMs OK.
- Learned about Additional Maps (optional content pack).

## Session 19 — “Hero” topics & control
- Observed topics use `/carla/hero/...` instead of `/carla/ego_vehicle/...` (naming from the example).
- Discussed control via `carla_manual_control` or publishing `/cmd_vel`, plus sensor visualization in RViz.

## Session 20 — `carla_manual_control` not found
- `ros2 run carla_manual_control carla_manual_control` failed—package not built/installed in the active env.
- Next steps: ensure `carla_manual_control` is in the workspace, rebuild, source `install/setup.bash`, then run; or run the example launch that already starts manual control.

---

## Quick Debrief

- ✅ **Solved:** compiler include path (`tf2_eigen`), duplicate packages, JSON format & spawnpoint validation, `empy`/`catkin_pkg` IDL issues, local CARLA dependencies, `carla_msgs` separate repo, Dockerfile for Foxy bridge, running CARLA 0.9.15 + bridge on host.  
- ⚠️ **Recurring pitfalls:** strict CARLA ↔ Python minor version match, mixing conda/venv/system Python, tag/branch confusion, container vs host graphics (Vulkan), blueprint not found when the bridge couldn’t properly connect or used a mismatched CARLA Python module.