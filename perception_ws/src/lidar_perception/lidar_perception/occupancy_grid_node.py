import math
import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2 as pc2
from nav_msgs.msg import OccupancyGrid


class OccupancyGridNode(Node):
    def __init__(self):
        super().__init__("occupancy_grid_node")

        self.resolution = 0.05
        self.width_m = 4.0
        self.height_m = 4.0

        self.width = int(self.width_m / self.resolution)
        self.height = int(self.height_m / self.resolution)

        self.origin_x = -self.width_m / 2.0
        self.origin_y = -self.height_m / 2.0

        self.sub = self.create_subscription(
            PointCloud2,
            "/flexirover/points",
            self.cloud_callback,
            10
        )

        self.pub = self.create_publisher(
            OccupancyGrid,
            "/perception/local_occupancy_grid",
            10
        )

        self.get_logger().info("Local occupancy grid node started.")

    def cloud_callback(self, msg: PointCloud2):
        grid = np.zeros((self.height, self.width), dtype=np.int8)

        for p in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True):
            x = float(p[0])
            y = float(p[1])

            # Ignore very close self-points
            if math.hypot(x, y) < 0.18:
                continue

            gx = int((x - self.origin_x) / self.resolution)
            gy = int((y - self.origin_y) / self.resolution)

            if 0 <= gx < self.width and 0 <= gy < self.height:
                grid[gy, gx] = 100

                # Inflate obstacles slightly
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ix = gx + dx
                        iy = gy + dy
                        if 0 <= ix < self.width and 0 <= iy < self.height:
                            grid[iy, ix] = 100

        msg_out = OccupancyGrid()
        msg_out.header.stamp = self.get_clock().now().to_msg()
        msg_out.header.frame_id = "flexirover/base_link/lidar"

        msg_out.info.resolution = self.resolution
        msg_out.info.width = self.width
        msg_out.info.height = self.height

        msg_out.info.origin.position.x = self.origin_x
        msg_out.info.origin.position.y = self.origin_y
        msg_out.info.origin.position.z = 0.0
        msg_out.info.origin.orientation.w = 1.0

        msg_out.data = grid.flatten().tolist()

        self.pub.publish(msg_out)


def main(args=None):
    rclpy.init(args=args)
    node = OccupancyGridNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
