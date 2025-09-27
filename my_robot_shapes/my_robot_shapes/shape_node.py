#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class shape_node(Node):
    def __init__(self):
        super().__init__('shape_node')
        self.publisher_ = self.create_publisher(String, 'shape_command', 10)
        self.get_logger().info('Shape Node is ready.')

    def publish_command(self, command):
        """Creates and publishes a String message."""
        msg = String()
        msg.data = command
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published command: "{command}"')

def main(args=None):
    rclpy.init(args=args)
    node = shape_node()

    while rclpy.ok():
        print("\n--- TurtleSim Shape Menu ---")
        print("  1: Draw a Car")
        print("  2: Draw a Robot")
        print("  3: Draw a Flower")
        print("  q: Quit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            node.publish_command('car')
        elif choice == '2':
            node.publish_command('robot')
        elif choice == '3':
            node.publish_command('flower')
        elif choice.lower() == 'q':
            print("Shutting down...")
            break
        else:
            print("Invalid choice, please try again.")
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

