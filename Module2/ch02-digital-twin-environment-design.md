---
id: ch02-digital-twin-environment-design
title: "Chapter 2: Digital Twin Environment Design"
description: "Learn how to design and build a digital twin environment in Gazebo."
tags: ["gazebo", "digital-twin", "urdf", "ros2", "sdf"]
---

## Learning Objectives

- Define the concept of a Digital Twin.
- Create a simple robot model using URDF.
- Build a Gazebo world with static objects.
- Spawn a robot model into a Gazebo world using a ROS 2 launch file.

## Introduction

In the previous chapter, you learned about the fundamentals of physics and collision modeling in Gazebo. Now, we will use that knowledge to create a complete digital twin environment. A digital twin is a virtual representation of a physical object or system, which can be used for simulation, testing, and development.

## Creating a Robot Model with URDF

The Unified Robot Description Format (URDF) is an XML format used to describe the kinematic and dynamic properties of a robot. A URDF file is composed of `<link>` and `<joint>` elements, which define the structure of the robot.

Here's an example of a simple two-wheeled robot described in URDF:

```xml
<robot name="my_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
    </collision>
  </link>

  <link name="left_wheel_link">
    ...
  </link>

  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel_link"/>
    ...
  </joint>
</robot>
```

- **`<link>`**: Represents a rigid body of the robot. It has `<visual>` and `<collision>` elements to define its appearance and collision geometry.
- **`<joint>`**: Connects two links and defines their relative motion.

## Building a Gazebo World

A Gazebo world is an SDF file (`.world`) that describes the environment in which the robot will be simulated. You can add static models (e.g., walls, furniture, obstacles) to the world from Gazebo's model database or by creating your own models.

Here's an example of a simple world file:

```xml
<sdf version="1.6">
  <world name="default">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
    <model name="box">
      <pose>0 5 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

- **`<world>`**: The root element of the world file.
- **`<include>`**: Includes a model from Gazebo's model database.
- **`<model>`**: Defines a custom model in the world.

## Spawning the Robot

Once you have a robot model and a world, you can use a ROS 2 launch file to start Gazebo and spawn the robot in the world.

The `spawn_entity.py` script, which is part of the `gazebo_ros` package, can be used to spawn a URDF model in Gazebo.

Here's an example of a launch file that starts Gazebo and spawns a robot:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', 'my_world.world'],
            output='screen'
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'my_robot', '-file', 'my_robot.urdf'],
            output='screen'
        )
    ])
```

## Conclusion

In this chapter, you have learned how to design and build a digital twin environment in Gazebo. You can now create your own robot models, build custom worlds, and spawn your robots in simulation. In the next chapter, we will explore how to visualize the digital twin in Unity and interact with it.

## References

- [URDF Documentation](http://wiki.ros.org/urdf)
- [Gazebo Tutorials](http://gazebosim.org/tutorials)
