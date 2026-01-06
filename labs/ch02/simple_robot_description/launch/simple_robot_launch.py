import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_simple_robot_description = get_package_share_directory('simple_robot_description')

    # Process the URDF file
    xacro_file = os.path.join(pkg_simple_robot_description, 'urdf', 'simple_arm.urdf')
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={'world': os.path.join(pkg_simple_robot_description, 'worlds', 'simple_world.world')}.items()
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_raw}]
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'simple_arm',
                '-topic', 'robot_description',
            ],
            output='screen'
        ),
    ])
