# Chapter 4: URDF for Humanoids

In the preceding chapters, we established the communication backbone of our robotic system using ROS 2 and implemented control logic with `rclpy`. Now, it's time to give our robot a physical form – at least in the digital realm. This chapter introduces the Unified Robot Description Format (URDF), a powerful XML-based language for describing the physical structure and properties of a robot. Understanding URDF is fundamental for simulating robots, planning their motions, and visualizing them in tools like RViz.

## Introduction to Robot Description Formats

Robots are complex machines with many interconnected parts, sensors, and actuators. To work with robots in simulation or control, we need a standardized way to describe their physical characteristics. This is where robot description formats come into play.

### What is URDF?

URDF stands for Unified Robot Description Format. It's an XML format used in ROS to describe all the physical aspects of a robot, including:
-   **Kinematics**: How the robot's links (rigid bodies) are connected by joints.
-   **Dynamics**: Properties like mass, inertia, and friction for each link and joint.
-   **Visuals**: How the robot looks (geometry, color, textures) for rendering in simulators and visualization tools.
-   **Collisions**: The geometry used for collision detection in simulation.

### Why URDF for Humanoid Robotics?

URDF is particularly well-suited for humanoid robotics due to its hierarchical structure and ability to define complex kinematic chains. Humanoids, with their many joints (degrees of freedom) mimicking human anatomy, benefit from URDF's clear definition of:
-   **Links**: Representing body segments (e.g., torso, upper arm, forearm, hand).
-   **Joints**: Defining the rotational or translational connections between these segments (e.g., shoulder, elbow, wrist).
-   **Tree Structure**: URDF inherently represents a robot as a tree structure, which is ideal for humanoids with a clear base link (e.g., the pelvis or torso) and branches extending to limbs.

### URDF vs SDF (Reiterate URDF focus)

While URDF is excellent for describing a single robot, a more comprehensive format called SDF (Simulation Description Format) is often used for describing entire simulation environments, including multiple robots, static objects (tables, walls), and environmental properties (gravity, lights). This module will exclusively focus on URDF, as it is the standard for defining robot models *within* ROS, and the conversion or integration with SDF for simulation is an advanced topic often handled by simulation tools themselves (e.g., Gazebo can import URDF and convert it to SDF internally).

## URDF Structure

A URDF file is essentially an XML document that starts with a `<robot>` tag. Inside this tag, you define all the robot's links and joints.

```xml
<?xml version="1.0"?>
<robot name="my_humanoid">
  <!-- Define links and joints here -->
  <link name="base_link">
    <!-- properties of the base_link -->
  </link>
  <joint name="joint_1" type="revolute">
    <!-- properties of joint_1 -->
  </joint>
</robot>
```

### `<robot>` Tag

The root element of every URDF file, taking a mandatory `name` attribute.

## Links: The Physical Parts

Links are the rigid bodies of your robot. They have physical properties and a geometric shape.

### `<link>` Tag

Each `<link>` tag represents a rigid body. Key elements within a link include:

-   `<visual>`: Defines how the link looks.
    -   `<geometry>`: Shape (box, cylinder, sphere, mesh) and its dimensions.
    -   `<material>`: Color (RGBa) or texture.
-   `<collision>`: Defines the geometry used for physics simulation and collision detection. Often simpler than the visual geometry to save computation.
-   `<inertial>`: Defines the mass and inertia properties of the link, crucial for realistic physics simulation.

**Example Link**:
```xml
<link name="torso">
  <visual>
    <geometry>
      <box size="0.1 0.2 0.3"/>
    </geometry>
    <material name="blue">
      <color rgba="0 0 1 1"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.1 0.2 0.3"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="1.0"/>
    <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
  </inertial>
</link>
```

## Joints: Connecting the Parts

Joints define how links are connected and how they can move relative to each other.

### `<joint>` Tag

Each `<joint>` tag connects two links: a `parent` link and a `child` link.

-   `name`: Unique name for the joint.
-   `type`: Type of motion allowed by the joint (e.g., `revolute`, `continuous`, `prismatic`, `fixed`).
-   `<parent link="parent_link_name"/>`: Specifies the parent link.
-   `<child link="child_link_name"/>`: Specifies the child link.
-   `<origin xyz="x y z" rpy="roll pitch yaw"/>`: Defines the joint's position and orientation relative to the parent link.
-   `<axis xyz="x y z"/>`: For rotational or translational joints, specifies the axis of motion.
-   `<limit lower="val" upper="val" effort="val" velocity="val"/>`: For revolute and prismatic joints, defines the range of motion, maximum effort, and maximum velocity.

**Example Joint**:
```xml
<joint name="shoulder_joint" type="revolute">
  <parent link="torso"/>
  <child link="upper_arm"/>
  <origin xyz="0.0 0.1 0.15" rpy="0 0 0"/>
  <axis xyz="1 0 0"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="10"/>
</joint>
```

## Building a Simple Humanoid Component (e.g., an arm)

Let's assemble a simple two-link arm for a humanoid.

### 1. Define the Base Link (e.g., `torso_link`)
```xml
<link name="torso_link">
  <visual>
    <geometry><box size="0.1 0.2 0.4"/></geometry>
    <material name="grey"><color rgba="0.7 0.7 0.7 1"/></material>
  </visual>
</link>
```

### 2. Define the First Arm Segment (e.g., `upper_arm_link`)
```xml
<link name="upper_arm_link">
  <visual>
    <geometry><cylinder radius="0.03" length="0.2"/></geometry>
    <material name="red"><color rgba="1 0 0 1"/></material>
  </visual>
</link>
```

### 3. Connect `torso_link` to `upper_arm_link` with a `shoulder_joint`
```xml
<joint name="shoulder_joint" type="revolute">
  <parent link="torso_link"/>
  <child link="upper_arm_link"/>
  <origin xyz="0 0.1 0.2" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="0.5"/>
</joint>
```

### 4. Define the Second Arm Segment (e.g., `forearm_link`)
```xml
<link name="forearm_link">
  <visual>
    <geometry><cylinder radius="0.025" length="0.15"/></geometry>
    <material name="green"><color rgba="0 1 0 1"/></material>
  </visual>
</link>
```

### 5. Connect `upper_arm_link` to `forearm_link` with an `elbow_joint`
```xml
<joint name="elbow_joint" type="revolute">
  <parent link="upper_arm_link"/>
  <child link="forearm_link"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="0.5"/>
</joint>
```

## Visualizing URDF with RViz

RViz (ROS Visualization) is the primary 3D visualization tool for ROS. It can load and display your URDF models, allowing you to verify their structure and see how joints move.

To visualize your URDF:
1.  Save your URDF XML content to a file (e.g., `my_arm.urdf`).
2.  Launch RViz: `ros2 run rviz2 rviz2`
3.  In RViz, add a "RobotModel" display.
4.  Set the "Robot Description" property to the content of your URDF file or a parameter that holds it.
5.  Use `joint_state_publisher_gui` to manipulate joint angles: `ros2 run joint_state_publisher_gui joint_state_publisher_gui`

This allows interactive debugging of your URDF model.

## Chapter Summary

This chapter introduced you to the Unified Robot Description Format (URDF), an essential tool for defining your robot's physical structure. You learned about links, joints, and how to combine them to create a simple humanoid arm. With this knowledge, you are now equipped to describe complex robots for simulation and control.