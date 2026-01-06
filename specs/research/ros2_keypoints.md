# ROS 2 Architecture: Key Points

This document synthesizes the key architectural concepts of ROS 2.

## 1. The ROS 2 Graph

The ROS 2 Graph is the network of ROS 2 nodes and their connections. Key elements include:

- **Nodes**: The primary computational units.
- **Topics**: For asynchronous, anonymous pub/sub communication.
- **Services**: For synchronous, request/reply communication.
- **Actions**: For long-running, feedback-enabled tasks.

## 2. DDS/RTPS Middleware

ROS 2 is built on top of the Data Distribution Service (DDS) standard, which provides a real-time, publish-subscribe middleware. This is a major departure from ROS 1's custom middleware.

## 3. Quality of Service (QoS)

QoS profiles allow for fine-grained control over the reliability, durability, and other aspects of communication. This is a key feature for building robust and reliable robotic systems.
