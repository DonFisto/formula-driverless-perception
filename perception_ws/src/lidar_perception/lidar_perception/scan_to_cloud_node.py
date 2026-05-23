import math
import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan, PointCloud2
from sensor_msgs_py import point_cloud2 as pc2


class ScanToCloudNode(Node):
    def __init__(self):
        super().__init__("scan_to_cloud_node")

        self.sub = self.create_subscription(
            LaserScan,
            "/flexirover/scan",
            self.scan_callback,
            10
        )

        self.pub = self.create_publisher(
            PointCloud2,
            "/flexirover/points",
            10
        )

        self.get_logger().info("Scan-to-cloud node started.")

    def scan_callback(self, msg: LaserScan):
        points = []

        angle = msg.angle_min

        for r in msg.ranges:
            if math.isfinite(r) and msg.range_min <= r <= msg.range_max:
                x = r * math.cos(angle)
                y = r * math.sin(angle)
                z = 0.0
                points.append((x, y, z))

            angle += msg.angle_increment

        cloud = pc2.create_cloud_xyz32(
            msg.header,
            points
        )

        self.pub.publish(cloud)


def main(args=None):
    rclpy.init(args=args)
    node = ScanToCloudNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
