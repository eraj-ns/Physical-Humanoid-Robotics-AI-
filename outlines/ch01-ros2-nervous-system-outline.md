# Module 1: The Robotic Nervous System (ROS 2) - Detailed Outline

## Introduction (Book/docs/Module1/intro.md)
- Welcome to Module 1: The Robotic Nervous System
- What is ROS 2?
- Why ROS 2 for humanoid robotics?
- Module objectives and learning outcomes

## Chapter 1: ROS 2 Architecture (Book/docs/Module1/ch01-ros2-architecture.md)
-   **Introduction to ROS 2**
    -   Evolution from ROS 1 to ROS 2 (brief overview of DDS)
    -   Key benefits of ROS 2 (real-time, security, multi-robot)
-   **Core Concepts**
    -   Nodes: The fundamental building blocks
    -   ROS Graph: Understanding the interconnected system
    -   DDS (Data Distribution Service): The middleware
    -   Quality of Service (QoS) policies (reliability, durability, history)
-   **ROS 2 Tooling Overview**
    -   `ros2 run`, `ros2 node`, `ros2 topic`, `ros2 service` (brief)
-   **Chapter Summary**

## Chapter 2: Nodes, Topics, Services (Book/docs/Module1/ch02-nodes-topics-services.md)
-   **Introduction to Communication Patterns**
-   **Nodes in Detail**
    -   Creating and launching nodes
    -   Node lifecycle (configure, activate, deactivate, cleanup)
-   **Topics for Asynchronous Communication**
    -   Publishers and Subscribers: How they work
    -   Message types: `std_msgs`, custom messages (brief)
    -   `ros2 topic` commands (`echo`, `list`, `info`, `pub`)
-   **Services for Synchronous Communication**
    -   Clients and Servers: Request/response model
    -   Service types
    -   `ros2 service` commands (`call`, `list`, `type`, `find`)
-   **Actions for Long-Running Tasks (Brief Introduction)**
    -   Goal, feedback, result
    -   `ros2 action` commands (brief)
-   **Chapter Summary**

## Chapter 3: Python Agents via rclpy (Book/docs/Module1/ch03-python-agents-rclpy.md)
-   **Introduction to `rclpy`**
    -   Why Python for ROS 2?
    -   `rclpy` vs `rclcpp` (reiterate `rclpy` focus)
-   **Creating a Simple `rclpy` Node**
    -   Basic node structure (`Node` class)
    -   Initializing and shutting down ROS 2
-   **Publishing Data with `rclpy`**
    -   Creating a publisher
    -   Sending messages
-   **Subscribing to Data with `rclpy`**
    -   Creating a subscriber
    -   Receiving and processing messages
-   **Implementing a Simple Service/Client**
    -   Service server implementation
    -   Service client implementation
-   **Building and Running `rclpy` Packages**
    -   `colcon build` basics
    -   `ros2 run` for Python nodes
-   **Chapter Summary**

## Chapter 4: URDF for Humanoids (Book/docs/Module1/ch04-urdf-for-humanoids.md)
-   **Introduction to Robot Description Formats**
    -   What is URDF?
    -   Why URDF for humanoid robotics?
    -   URDF vs SDF (reiterate URDF focus)
-   **URDF Structure**
    -   XML syntax
    -   `<robot>` tag
-   **Links: The Physical Parts**
    -   `<link>` tag (visual, collision, inertial properties)
    -   Geometric primitives (box, cylinder, sphere, mesh)
-   **Joints: Connecting the Parts**
    -   `<joint>` tag (parent/child links, origin, axis, type)
    -   Types of joints (revolute, prismatic, fixed)
-   **Building a Simple Humanoid Component (e.g., an arm)**
    -   Step-by-step creation of a multi-link, multi-joint model
    -   Adding visual and collision properties
-   **Visualizing URDF with RViz**
    -   Using `urdf_tutorial` or `joint_state_publisher`
    -   Debugging URDF models
-   **Chapter Summary**

## Conclusion to Module 1
- Recap of key learnings
- What's next? (Transition to Module 2)
