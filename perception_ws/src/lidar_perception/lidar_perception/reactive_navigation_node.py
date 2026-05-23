import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class ReactiveNavigationNode(Node):
    def __init__(self):
        super().__init__("reactive_navigation_node")

        self.forward_speed = 0.16
        self.slow_speed = 0.05
        self.backup_speed = -0.10
        self.turn_speed = 0.70

        self.front_width = math.radians(35)
        self.side_width = math.radians(50)
        self.side_angle = math.radians(65)

        self.danger_distance = 0.45
        self.clear_distance = 0.85
        self.backup_distance = 0.30

        self.backup_duration = 0.8
        self.min_turn_duration = 0.8
        self.max_turn_duration = 2.5

        self.state = "FORWARD"
        self.state_start = self.now_ns()
        self.turn_dir = 1.0

        self.last_scan = None

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)

        self.scan_sub = self.create_subscription(
            LaserScan,
            "/flexirover/scan",
            self.scan_callback,
            10
        )

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info("Front-corridor reactive navigation started.")

    def now_ns(self):
        return self.get_clock().now().nanoseconds

    def elapsed(self):
        return (self.now_ns() - self.state_start) / 1e9

    def set_state(self, state):
        self.state = state
        self.state_start = self.now_ns()

    def scan_callback(self, msg):
        self.last_scan = msg

    def normalize_angle(self, a):
        while a > math.pi:
            a -= 2.0 * math.pi
        while a < -math.pi:
            a += 2.0 * math.pi
        return a

    def sector_clearance(self, scan, center, width):
        vals = []
        angle = scan.angle_min

        for r in scan.ranges:
            if math.isfinite(r) and scan.range_min <= r <= scan.range_max:
                if abs(self.normalize_angle(angle - center)) <= width / 2.0:
                    vals.append(r)
            angle += scan.angle_increment

        if not vals:
            return scan.range_max

        vals.sort()

        # Low percentile, robust against a few long rays.
        idx = max(0, int(0.20 * len(vals)) - 1)
        return vals[idx]

    def choose_turn_dir(self, scan):
        left = self.sector_clearance(scan, self.side_angle, self.side_width)
        right = self.sector_clearance(scan, -self.side_angle, self.side_width)

        # Positive angular.z = turn left.
        if left > right:
            return 1.0
        else:
            return -1.0

    def publish_cmd(self, vx, wz):
        cmd = Twist()
        cmd.linear.x = vx
        cmd.angular.z = wz
        self.cmd_pub.publish(cmd)

    def timer_callback(self):
        if self.last_scan is None:
            self.publish_cmd(0.0, 0.0)
            return

        scan = self.last_scan

        front = self.sector_clearance(scan, 0.0, self.front_width)
        left = self.sector_clearance(scan, self.side_angle, self.side_width)
        right = self.sector_clearance(scan, -self.side_angle, self.side_width)

        if self.state == "FORWARD":
            if front < self.backup_distance:
                self.turn_dir = self.choose_turn_dir(scan)
                self.set_state("BACKUP")
            elif front < self.danger_distance:
                self.turn_dir = self.choose_turn_dir(scan)
                self.set_state("TURN")
            else:
                self.publish_cmd(self.forward_speed, 0.0)
                return

        if self.state == "BACKUP":
            if self.elapsed() < self.backup_duration:
                self.publish_cmd(self.backup_speed, 0.0)
                return
            self.set_state("TURN")

        if self.state == "TURN":
            front_clear = front > self.clear_distance
            enough_time = self.elapsed() > self.min_turn_duration
            too_long = self.elapsed() > self.max_turn_duration

            if enough_time and front_clear:
                self.set_state("FORWARD")
                self.publish_cmd(self.slow_speed, 0.0)
                return

            if too_long:
                # If still blocked after a long turn, back up and try again.
                self.turn_dir = self.choose_turn_dir(scan)
                self.set_state("BACKUP")
                self.publish_cmd(self.backup_speed, 0.0)
                return

            self.publish_cmd(0.0, self.turn_dir * self.turn_speed)
            return

        self.get_logger().info(
            f"state={self.state} front={front:.2f} left={left:.2f} right={right:.2f} turn={self.turn_dir:+.0f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = ReactiveNavigationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publish_cmd(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
