from perception_msgs.msg import Obstacle, ObstacleArray
import math
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2 as pc2
from visualization_msgs.msg import Marker, MarkerArray
from sklearn.cluster import DBSCAN
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

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


def normalize_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


def smooth_angle(prev: float, curr: float, alpha: float) -> float:
    diff = normalize_angle(curr - prev)
    return normalize_angle(prev + alpha * diff)


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

    if np.allclose(centered, 0.0):
        return None, None, None, None

    cov = np.cov(centered.T)

    if np.any(np.isnan(cov)) or np.any(np.isinf(cov)):
        return None, None, None, None

    eigvals, eigvecs = np.linalg.eigh(cov)
    principal_axis = eigvecs[:, np.argmax(eigvals)]
    yaw = math.atan2(principal_axis[1], principal_axis[0])

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

        self.alpha = 0.3
        self.prev_boxes = {}

        self.sub = self.create_subscription(
            PointCloud2,
            "/flexirover/points",
            self.cb,
            10
        )
        marker_qos = QoSProfile(
          history=HistoryPolicy.KEEP_LAST,
          depth=10,
          reliability=ReliabilityPolicy.RELIABLE,
          durability=DurabilityPolicy.TRANSIENT_LOCAL
        )

        self.pub_markers = self.create_publisher(
            MarkerArray,
            "/perception/obstacles_obb",
            10
        )

        self.pub_obstacles = self.create_publisher(
            ObstacleArray,
            "/perception/obstacles",
            10
        )

        self.get_logger().info("OBB obstacle node started.")

    def cb(self, msg):
        pts = pc2_to_xyz(msg)
        if pts.shape[0] == 0:
            return

        # Only apply ground filter if there is meaningful Z variation
        if (pts[:, 2].max() - pts[:, 2].min()) > 0.1:
            pts = pts[pts[:, 2] > 0.2]

        pts = voxel_downsample_xyz(pts, voxel_size=0.10)

        if pts.shape[0] == 0:
            return

        labels = DBSCAN(eps=0.25, min_samples=4).fit_predict(pts[:, :2])
        unique_labels = set(labels)

        now = self.get_clock().now().to_msg()
        frame = msg.header.frame_id if msg.header.frame_id else "lidar_link"

        ma = MarkerArray()

        delete_marker = Marker()
        delete_marker.action = Marker.DELETEALL
        ma.markers.append(delete_marker)

        obstacle_array = ObstacleArray()
        obstacle_array.header.stamp = now
        obstacle_array.header.frame_id = frame

        marker_id = 0
        for lab in unique_labels:
            if lab == -1:
                continue

            cluster = pts[labels == lab]

            if cluster.shape[0] < 4:
                continue

            cluster_xy = cluster[:, :2]
            result = compute_obb_2d(cluster_xy)

            if result[0] is None:
                continue

            center_xy, yaw, sx, sy = result

            zmin = cluster[:, 2].min()
            zmax = cluster[:, 2].max()
            cz = 0.5 * (zmax + zmin)
            sz = 0.15

            # EMA smoothing
            curr_center = np.array([center_xy[0], center_xy[1], cz], dtype=np.float32)
            curr_size = np.array([sx, sy, sz], dtype=np.float32)

            key = int(lab)

            if key in self.prev_boxes:
                prev = self.prev_boxes[key]

                smooth_center = (
                    self.alpha * curr_center +
                    (1.0 - self.alpha) * prev["center"]
                )

                smooth_size = (
                    self.alpha * curr_size +
                    (1.0 - self.alpha) * prev["size"]
                )

                smooth_yaw = smooth_angle(prev["yaw"], yaw, self.alpha)
            else:
                smooth_center = curr_center
                smooth_size = curr_size
                smooth_yaw = yaw

            self.prev_boxes[key] = {
                "center": smooth_center,
                "size": smooth_size,
                "yaw": smooth_yaw
            }

            # ---------- Marker ----------
            qx, qy, qz, qw = yaw_to_quaternion(smooth_yaw)

            m = Marker()
            m.header.frame_id = frame
            m.header.stamp = now
            m.ns = "obb"
            m.id = int(marker_id)
            marker_id += 1
            m.type = Marker.CUBE
            m.action = Marker.ADD

            m.pose.position.x = float(smooth_center[0])
            m.pose.position.y = float(smooth_center[1])
            m.pose.position.z = float(smooth_center[2]) + float(smooth_size[2]) / 2.0

            m.pose.orientation.x = qx
            m.pose.orientation.y = qy
            m.pose.orientation.z = qz
            m.pose.orientation.w = qw

            m.scale.x = float(smooth_size[0])
            m.scale.y = float(smooth_size[1])
            m.scale.z = float(smooth_size[2])

            m.color.r = 0.0
            m.color.g = 0.8
            m.color.b = 0.3
            m.color.a = 0.45

            m.lifetime.sec = 0
            m.lifetime.nanosec = 300000000

            ma.markers.append(m)

            # ---------- Structured obstacle ----------
            obs = Obstacle()
            obs.x = float(smooth_center[0])
            obs.y = float(smooth_center[1])
            obs.sx = float(smooth_size[0])
            obs.sy = float(smooth_size[1])
            obs.yaw = float(smooth_yaw)

            obstacle_array.obstacles.append(obs)

        valid_ids = {int(l) for l in unique_labels if l != -1}
        self.prev_boxes = {k: v for k, v in self.prev_boxes.items() if k in valid_ids}

        self.pub_markers.publish(ma)
        self.pub_obstacles.publish(obstacle_array)


def main():
    rclpy.init()
    node = LidarObstacleNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
