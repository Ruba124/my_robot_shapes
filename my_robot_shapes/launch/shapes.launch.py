from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),
        Node(
            package='my_robot_shapes',
            executable='turtle_commander',
            name='turtle_commander'
        ),
        Node(
             package='my_robot_shapes', # Or your actual package name
             executable='shape_node',   # Or your actual executable name
             name='shape_node',
             output='screen',
             prefix='xterm -e'  # <-- ADD THIS LINE
),
    ])
