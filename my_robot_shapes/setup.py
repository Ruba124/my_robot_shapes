import os
from setuptools import find_packages, setup
from glob import glob

package_name = 'my_robot_shapes'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ruba124x',
    maintainer_email='ruba124x@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'shape_node = my_robot_shapes.shape_node:main',
            'turtle_commander = my_robot_shapes.turtle_commander:main'
        ],
    },
)
