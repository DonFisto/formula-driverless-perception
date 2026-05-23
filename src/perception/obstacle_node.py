import math
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2 as pc2
from visualization_msgs.msg import Marker, MarkerArray
from sklearn.cluster import DBSCAN


def pc2_to_xyz(msg):
    pts = []
    for p in pc2.read_points(msg, field_names=('x', 'y', 'z'), skip_nans=True):
        pts.append((p[0], p[1], p[2]))
    return np.array(pts, dtype=np.float32)


def voxel_downsample_xyz(pts: np.ndarray, voxel_size: float) -> np.ndarray:
    if pts.shape[0] == 0:
        return pts

    vs = float(voxel_size)
    q = np.floor(pts / vs).astype(np.int32)
    _, inv = np.unique(q, axis=0, return_inverse=True)

    out = np.zeros((inv.max() + 1, 3), dtype=np.float32)
    counts = np.bincount(inv)
    np.add.at(out, inv, pts)
    out /= counts[:, None].astype(np.float32)
    return out


def yaw_to_quaternion(yaw: float):
    qx = 0.0
    qy = 0.0
    qz = math.sin(yaw / 2.0)
    qw = math.cos(yaw / 2.0)
    return qx, qy, qz, qw


def compute_obb_2d(cluster_xy: np.ndarray):
    """
    Compute a 2D OBB from XY points using PCA.

    Returns:
        center_xy: np.array([cx, cy])
        yaw: float
        sx: float
        sy: float
    """
    if cluster_xy.shape[0] < 3:
        return None, None, None, None

    mean = np.mean(cluster_xy, axis=0)
    centered = cluster_xy - mean

    # If points are degenerate, covariance/PCA can be unstable
    if np.allclose(centered, 0.0):
        return None, None, None, None

    cov = np.cov(centered.T)

    # Guard against numerical issues
    if np.any(np.isnan(cov)) or np.any(np.isinf(cov)):
        return None, None, None, None

    eigvals, eigvecs = np.linalg.eigh(cov)
    principal_axis = eigvecs[:, np.argmax(eigvals)]
    yaw = math.atan2(principal_axis[1], principal_axis[0])

    # Rotate points into local OBB frame
    c = math.cos(-yaw)
    s = math.sin(-yaw)
    R = np.array([[c, -s],
                  [s,  c]], dtype=np.float32)

    rotated = (cluster_xy - mean) @ R.T

    xmin, ymin = rotated.min(axis=0)
    xmax, ymax = rotated.max(axis=0)

    sx = max(0.05, float(xmax - xmin))
    sy = max(0.05, float(ymax - ymin))

    local_center = np.array(
        [(xmin + xmax) / 2.0, (ymin + ymax) / 2.0],
        dtype=np.float32
    )

    c2 = math.cos(yaw)
    s2 = math.sin(yaw)
    R_inv = np.array([[c2, -s2],
                      [s2,  c2]], dtype=np.float32)

    world_center = mean + local_center @ R_inv.T

    return world_center, yaw, sx, sy


class LidarObstacleNode(Node):
    def __init__(self):
        super().__init__('lidar_obstacle_node')

        self.sub = self.create_subscription(
            PointCloud2,
            "/flexirover/points",
            self.cb,
            10
        )

        self.pub = self.create_publisher(
            MarkerArray,
            "/perception/obstacles_obb",
            10
        )

        self.get_logger().info("OBB obstacle node started.")

    def cb(self, msg):
        self.get_logger().info("OBB callback triggered")

        pts = pc2_to_xyz(msg)
        if pts.shape[0] == 0:
            self.get_logger().info("No points received.")
            return

        # Only apply ground filter if there is meaningful Z variation
        if (pts[:, 2].max() - pts[:, 2].min()) > 0.1:
            pts = pts[pts[:, 2] > 0.2]

        pts = voxel_downsample_xyz(pts, voxel_size=0.10)

        if pts.shape[0] == 0:
            self.get_logger().info("No points left after downsampling/filtering.")
            return

        self.get_logger().info(f"Points after downsampling: {pts.shape[0]}")

        # Relaxed parameters for current 2D Gazebo LiDAR
        labels = DBSCAN(eps=0.5, min_samples=4).fit_predict(pts[:, :2])
        unique_labels = set(labels)
        self.get_logger().info(f"Unique labels: {unique_labels}")

        ma = MarkerArray()
        now = self.get_clock().now().to_msg()
        frame = msg.header.frame_id if msg.header.frame_id else "lidar_link"

        marker_id = 0
        for lab in unique_labels:
            if lab == -1:
                continue

            cluster = pts[labels == lab]

            # Relaxed cluster-size filtering
            if cluster.shape[0] < 4:
                continue

            cluster_xy = cluster[:, :2]
            result = compute_obb_2d(cluster_xy)

            if result[0] is None:
                continue

            center_xy, yaw, sx, sy = result

            # Use fixed height for visibility in RViz
            zmin = cluster[:, 2].min()
            zmax = cluster[:, 2].max()
            cz = 0.5 * (zmax + zmin)
            sz = 0.30

            qx, qy, qz, qw = yaw_to_quaternion(yaw)

            m = Marker()
            m.header.frame_id = frame
            m.header.stamp = now
            m.ns = "obb"
            m.id = int(marker_id)
            marker_id += 1
            m.type = Marker.CUBE
            m.action = Marker.ADD

            m.pose.position.x = float(center_xy[0])
            m.pose.position.y = float(center_xy[1])
            m.pose.position.z = float(cz) + sz / 2.0

            m.pose.orientation.x = qx
            m.pose.orientation.y = qy
            m.pose.orientation.z = qz
            m.pose.orientation.w = qw

            m.scale.x = sx
            m.scale.y = sy
            m.scale.z = sz

            m.color.r = 0.0
            m.color.g = 0.8
            m.color.b = 0.3
            m.color.a = 0.45

            # Disable auto-expire for debugging
            m.lifetime.sec = 0
            m.lifetime.nanosec = 0

            ma.markers.append(m)

        self.get_logger().info(f"Publishing {len(ma.markers)} OBB markers")
        self.pub.publish(ma)


def main():
    rclpy.init()
    node = LidarObstacleNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
