---
id: specs-008-ros2-nervous-system-research-ros2_keypoints
---
# ROS 2 Key Concepts and Architecture

This document synthesizes core concepts of ROS 2, forming the basis for Module 1, Chapter 1.

## Core Concepts

1.  **Nodes**:
    *   **Definition**: Executable processes that perform computation (e.g., a sensor driver, a controller, a planning algorithm).
    *   **Autonomy**: Each node is an independent module.
    *   **Communication**: Nodes communicate with each other using various mechanisms.

2.  **Topics**:
    *   **Definition**: A bus for asynchronous, one-way streaming of data.
    *   **Publish/Subscribe**: Nodes publish messages to topics, and other nodes subscribe to topics to receive messages.
    *   **Loose Coupling**: Publishers and subscribers do not need to know about each other's existence.
    *   **Message Types**: Data transmitted over topics are strongly typed (e.g., `std_msgs/msg/String`, `sensor_msgs/msg/Image`).

3.  **Services**:
    *   **Definition**: A mechanism for synchronous, request-response communication between nodes.
    *   **Client/Server**: A client sends a request to a server, and the server processes the request and sends a response back to the client.
    *   **Blocking**: The client typically blocks until it receives a response.

4.  **Actions**:
    *   **Definition**: A long-running, asynchronous communication mechanism for goal-oriented tasks.
    *   **Goal/Feedback/Result**: An action client sends a goal, receives continuous feedback on the progress, and eventually a final result.
    *   **Preemptable**: Goals can be canceled or preempted during execution.

5.  **Parameters**:
    *   **Definition**: Dynamic configuration values for nodes.
    *   **Runtime Adjustment**: Parameters can be changed at runtime without restarting the node.

6.  **ROS 2 Graph**:
    *   **Definition**: The network of ROS 2 nodes and their connections (topics, services, actions, parameters).
    *   **Decentralized**: Unlike ROS 1's single `roscore`, ROS 2 is decentralized due to DDS.

## Architecture and Middleware

1.  **DDS (Data Distribution Service)**:
    *   **Core of ROS 2**: Replaced ROS 1's custom TCP/IP-based communication layer.
    *   **Vendor Agnostic**: ROS 2 supports multiple DDS implementations (e.g., Fast RTPS, Cyclone DDS).
    *   **Qualities of Service (QoS)**: DDS provides configurable QoS policies (e.g., reliability, durability, history, deadline) for fine-grained control over communication.

2.  **`rcl` (ROS Client Library) Interface**:
    *   **Common API**: A C API that provides a common interface for implementing client libraries in different languages (e.g., `rclpy` for Python, `rclcpp` for C++).
    *   **Language Agnostic**: Ensures consistent behavior across different programming languages.

3.  **Client Libraries (`rclpy`, `rclcpp`)**:
    *   **`rclpy`**: Python client library, built on `rcl`. Eases ROS 2 development for Python users.
    *   **`rclcpp`**: C++ client library, built on `rcl`. Provides high-performance ROS 2 development for C++ users.

## Communication Patterns

1.  **One-to-Many Asynchronous (Topics)**: For sensor data, robot state, etc.
2.  **One-to-One Synchronous (Services)**: For requesting specific actions or information.
3.  **One-to-One Long-Running Asynchronous (Actions)**: For complex tasks like navigation or manipulation.
