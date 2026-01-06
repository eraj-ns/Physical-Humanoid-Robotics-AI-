# Unity Visualization for Digital Twin

This document provides instructions on how to set up a Unity project to visualize the digital twin of the simple robot arm simulated in Gazebo.

## Prerequisites

- Unity Hub and Unity Editor (2020.3 or later)
- [ROS#](https://github.com/siemens/ros-sharp) library

## Setup Instructions

1.  **Create a new Unity project**: Open Unity Hub and create a new 3D project.

2.  **Import ROS#**:
    - Download the latest `RosSharp.unitypackage` from the [ROS# releases page](https://github.com/siemens/ros-sharp/releases).
    - In your Unity project, go to `Assets > Import Package > Custom Package...` and select the downloaded `RosSharp.unitypackage`.

3.  **Import the Robot Model**:
    - You will need to convert the `simple_arm.urdf` file to a format that Unity can use (e.g., FBX). You can use the [URDF Importer](https://github.com/Unity-Technologies/URDF-Importer) Unity package for this.
    - Import the generated FBX model into your Unity project.

4.  **Configure ROS#**:
    - In the Unity Editor, go to `ROS# > RosBridgeClient > Set RosBridgeClient settings`.
    - Set the `ROS Bridge Server Ip` to the IP address of the machine running the ROS 2 network. If you are running everything on the same machine, you can use `localhost`.
    - Set the `ROS Bridge Server Port` to `9090` (the default for `ros2-web-bridge`).

5.  **Create a ROS Connector GameObject**:
    - Create an empty GameObject in your scene and name it `RosConnector`.
    - Attach the `RosConnector.cs` script (provided in this directory) to this GameObject.
    - In the Inspector for the `RosConnector` GameObject, you will see fields to specify the ROS topic names for the robot's joint states. Set these to the appropriate topic names from your ROS 2 network (e.g., `/joint_states`).

6.  **Run the Simulation**:
    - Launch the Gazebo simulation with the simple robot arm using the launch file from `labs/ch02`.
    - Start the `ros2-web-bridge` to connect ROS 2 to ROS#: `ros2 run rosbridge_server rosbridge_websocket`.
    - Press the Play button in the Unity Editor to start the visualization.

You should now see the robot arm in Unity, and its movements should mirror the movements in the Gazebo simulation.
