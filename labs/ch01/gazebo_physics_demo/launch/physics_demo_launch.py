import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_gazebo_physics_demo = get_package_share_directory('gazebo_physics_demo')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={'world': os.path.join(pkg_gazebo_physics_demo, 'worlds', 'physics_demo.world')}.items()
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'cube',
                '-file', os.path.join(pkg_gazebo_physics_demo, 'urdf', 'cube.urdf'),
            ],
            output='screen'
        ),
    ])
