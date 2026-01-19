import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2 as pc2
from visualization_msgs.msg import Marker, MarkerArray
from sklearn.cluster import DBSCAN

def pc2_to_xyz(msg):
    pts = []
    for p in pc2.read_points(msg, field_names=('x','y','z'), skip_nans=True):
        pts.append((p[0], p[1], p[2]))
    return np.array(pts, dtype=np.float32)

class LidarObstacleNode(Node):
    def __init__(self):
        super().__init__('lidar_obstacle_node')
        self.sub = self.create_subscription(PointCloud2, "/gazebo_ros_laser/out", self.cb, 10)
        self.pub = self.create_publisher(MarkerArray, "/perception/obstacles", 10)

    def cb(self, msg):
        pts = pc2_to_xyz(msg)
        if pts.shape[0] == 0:
            return
        # ground filter: keep z > 0.2
        pts = pts[pts[:,2] > 0.2]
        if pts.shape[0] == 0:
            return
        # clustering
        labels = DBSCAN(eps=0.7, min_samples=10).fit_predict(pts[:,:2])
        ma = MarkerArray()
        #First version
        for i in set(labels):
            if i == -1: continue
            cluster = pts[labels==i]
            center = cluster.mean(axis=0)
            marker = Marker()
            marker.header.frame_id = msg.header.frame_id or "lidar_link"
            marker.id = int(i)
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position.x = float(center[0])
            marker.pose.position.y = float(center[1])
            marker.pose.position.z = float(center[2])
            marker.scale.x = marker.scale.y = marker.scale.z = 1.0
            marker.color.r, marker.color.g, marker.color.b, marker.color.a = 0.0, 0.0, 1.0, 0.8
            ma.markers.append(marker)
        self.pub.publish(ma)

def main():
    rclpy.init()
    node = LidarObstacleNode()
    rclpy.spin(node)
    rclpy.shutdown()
