#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from turtlesim.srv import TeleportAbsolute, SetPen
# IMPORT THE SERVICE FOR CLEARING THE SCREEN
from std_srvs.srv import Empty 
import math, time

class TurtleCommander(Node):
    def __init__(self):
        super().__init__('turtle_commander')

        # Subscribers
        self.subscriber = self.create_subscription(
            String, 'shape_command', self.listener_callback, 10
        )

        # Service clients
        self.tp_cli = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_cli = self.create_client(SetPen, '/turtle1/set_pen')
        # CREATE THE CLIENT FOR THE /clear SERVICE
        self.clear_cli = self.create_client(Empty, 'clear')

        while not self.tp_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for teleport service...")
        while not self.pen_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for set_pen service...")
        # WAIT FOR THE CLEAR SERVICE
        while not self.clear_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for clear service...")

        self.get_logger().info("TurtleCommander ready. Waiting for commands...")

    # ------------------- CALLBACK -------------------
    def listener_callback(self, msg):
        cmd = msg.data.lower()
        self.get_logger().info(f"Received command: {cmd}")

        if cmd == "car":
            self.draw_car()
        elif cmd == "robot":
            self.draw_robot()
        elif cmd == "flower":
            self.draw_flower()
        elif cmd == "stop":
            self.get_logger().info("Stop command received.")
        else:
            self.get_logger().warn("Unknown command!")
        
        # Call the clear function *after* any valid drawing command has finished
        if cmd in ["car", "robot", "flower"]:
            self.clear_screen()

    # ------------------- CLEAR SCREEN FUNCTION -------------------
    def clear_screen(self):
        """Calls the /clear service to wipe the turtlesim window."""
        self.get_logger().info("Drawing finished. Clearing turtlesim screen...")
        req = Empty.Request()
        self.clear_cli.call_async(req)
        # Note: You generally don't need to wait for the response for the /clear service.

    # ------------------- HELPERS -------------------
    def set_pen(self, r, g, b, width=2, off=0):
        # ... (unchanged)
        req = SetPen.Request()
        req.r, req.g, req.b = r, g, b
        req.width, req.off = width, off
        self.pen_cli.call_async(req)
        time.sleep(0.05)

    def teleport(self, x, y, theta=0.0):
        # ... (unchanged)
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = float(x), float(y), float(theta)
        self.tp_cli.call_async(req)
        time.sleep(0.02)

    # ------------------- CAR -------------------
    def draw_rectangle(self, x1, y1, x2, y2, color):
        # ... (unchanged)
        r,g,b = color
        self.set_pen(r,g,b,2,1); self.teleport(x1,y1); self.set_pen(r,g,b,2,0)
        for x in [i*0.1 for i in range(int(x1*10), int(x2*10))]: self.teleport(x,y1)
        for y in [i*0.1 for i in range(int(y1*10), int(y2*10))]: self.teleport(x2,y)
        for x in [i*0.1 for i in range(int(x2*10), int(x1*10), -1)]: self.teleport(x,y2)
        for y in [i*0.1 for i in range(int(y2*10), int(y1*10), -1)]: self.teleport(x1,y)

    def draw_circle(self, cx, cy, r, color):
        # ... (unchanged)
        cr,cg,cb = color
        self.set_pen(cr,cg,cb,2,1); self.teleport(cx+r,cy); self.set_pen(cr,cg,cb,2,0)
        for deg in range(0,361,5):
            rad=math.radians(deg)
            self.teleport(cx+r*math.cos(rad), cy+r*math.sin(rad))

    def draw_roof_step(self):
        self.set_pen(200,200,200,2,1); self.teleport(2.5,4.0); self.set_pen(200,200,200,2,0)
        self.teleport(4.0,4.0); time.sleep(0.1) # Added sleep
        self.teleport(4.0,5.0); time.sleep(0.1) # Added sleep
        self.teleport(5.5,5.0); time.sleep(0.1) # Added sleep
        self.teleport(6.0,4.0); time.sleep(0.3) # Added sleep
        self.teleport(2.5,4.0); time.sleep(0.4) # Added sleep

    def draw_car(self):
        self.get_logger().info("Drawing car...")
        self.draw_rectangle(2.0,2.0,6.0,4.0,(0,0,255))
        self.draw_circle(2.5,1.5,0.5,(0,0,0)); self.draw_circle(5.5,1.5,0.5,(0,0,0))
        self.draw_roof_step()

    # ------------------- ROBOT -------------------
    def draw_arc(self, cx, cy, r, start_deg, end_deg, color):
        # ... (unchanged)
        r_,g_,b_=color
        self.set_pen(r_,g_,b_,2,1)
        self.teleport(cx+r*math.cos(math.radians(start_deg)), cy+r*math.sin(math.radians(start_deg)))
        self.set_pen(r_,g_,b_,2,0)
        for deg in range(start_deg,end_deg+1,5):
            rad=math.radians(deg)
            self.teleport(cx+r*math.cos(rad), cy+r*math.sin(rad))

    def draw_robot(self):
        self.get_logger().info("Drawing robot...")
        self.draw_rectangle(3.5,4,7.5,7.5,(210,180,140))  # body
        self.draw_rectangle(3.5,7.5,7.5,10,(210,180,140)) # head
        self.draw_circle(4.3,9.2,0.25,(0,0,0)); self.draw_circle(6.7,9.2,0.25,(0,0,0)) # eyes
        self.draw_arc(5.5,8.5,0.4,200,340,(0,0,0)) # mouth
        self.draw_rectangle(3.3,9.5,3.7,10,(210,180,140)); self.draw_rectangle(7.3,9.5,7.7,10,(210,180,140)) # ears
        self.draw_rectangle(3,6,3.5,6.7,(210,180,140)); self.draw_rectangle(7.5,6,8,6.7,(210,180,140)) # arms
        self.draw_rectangle(4.3,3,4.7,4,(210,180,140)); self.draw_rectangle(6.3,3,6.7,4,(210,180,140)) # legs
        self.draw_circle(4.5,2.5,0.4,(80,80,80)); self.draw_circle(6.5,2.5,0.4,(80,80,80)) # wheels

    # ------------------- FLOWER -------------------
    def draw_flower(self):
        self.get_logger().info("Drawing flower...")
        cx, cy = 5.5, 5.5     # flower center
        a, b, d = 1.2, 0.5, 1.0
        n_petals = 8
        petal_color = (139, 69, 19)  # brown

        for k in range(n_petals):
            theta = 2.0 * math.pi * k / n_petals
            x_local = a * math.cos(0.0)
            y_local = b * math.sin(0.0)
            x_rot = math.cos(theta) * x_local - math.sin(theta) * y_local
            y_rot = math.sin(theta) * x_local + math.cos(theta) * y_local
            start_x = cx + d * math.cos(theta) + x_rot
            start_y = cy + d * math.sin(theta) + y_rot
            self.set_pen(0, 0, 0, 1, off=1)
            self.teleport(start_x, start_y)
            self.set_pen(*petal_color, 2, off=0)
            for i in range(1, 41):
                t = 2.0 * math.pi * i / 40
                x_local = a * math.cos(t)
                y_local = b * math.sin(t)
                x_rot = math.cos(theta) * x_local - math.sin(theta) * y_local
                y_rot = math.sin(theta) * x_local + math.cos(theta) * y_local
                x = cx + d * math.cos(theta) + x_rot
                y = cy + d * math.sin(theta) + y_rot
                self.teleport(x, y)
            self.set_pen(0, 0, 0, 1, off=1)
        r = 0.7
        self.set_pen(0, 0, 0, 1, off=1)
        self.teleport(cx + r, cy)
        self.set_pen(255, 255, 0, 3, off=0)
        for i in range(1, 81):
            t = 2.0 * math.pi * i / 80
            x = cx + r * math.cos(t)
            y = cy + r * math.sin(t)
            self.teleport(x, y)
        self.set_pen(0, 0, 0, 1, off=1)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleCommander()
    rclpy.spin(node)
    node.destroy_node() # Good practice to destroy node before shutdown
    rclpy.shutdown()

if __name__ == '__main__':
    main()
