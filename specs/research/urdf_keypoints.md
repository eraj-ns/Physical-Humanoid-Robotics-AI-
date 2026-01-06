# URDF & Kinematics: Key Points

This document synthesizes the key concepts of URDF and kinematics.

## 1. URDF Structure

A URDF file is an XML file with the following main elements:

- **`<robot>`**: The root element of the URDF file.
- **`<link>`**: Describes a rigid part of the robot.
  - **`<visual>`**: Defines the visual representation of the link.
  - **`<collision>`**: Defines the collision geometry of the link.
  - **`<inertial>`**: Defines the inertial properties of the link (mass, moment of inertia).
- **`<joint>`**: Describes the connection between two links.
  - **`type`**: Can be `revolute`, `continuous`, `prismatic`, `fixed`, `floating`, or `planar`.
  - **`<parent>`** and **`<child>`**: The two links connected by the joint.
  - **`<axis>`**: The axis of rotation or translation for the joint.
  - **`<limit>`**: Defines the joint limits (for revolute and prismatic joints).

## 2. Kinematics

- **Forward Kinematics**: Given the joint angles, calculate the position and orientation of the end-effector.
- **Inverse Kinematics**: Given the position and orientation of the end-effector, calculate the required joint angles. This is a much harder problem and often has multiple solutions or no solution.
