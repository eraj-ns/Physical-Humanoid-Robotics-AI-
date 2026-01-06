---
id: specs-008-ros2-nervous-system-research
---
# Research: Module 1: The Robotic Nervous System (ROS 2) Development

This document outlines the decisions made for the development of "Module 1: The Robotic Nervous System (ROS 2)". These decisions were made based on user clarification and best practices for a foundational textbook module.

## 1. ROS 2 Versioning

-   **Decision**: Target ROS 2 Humble, with notes for newer versions.
-   **Rationale**: ROS 2 Humble is an LTS (Long Term Support) release, offering a stable and widely adopted base, which is ideal for educational material. Including notes for newer versions acknowledges the rapid evolution of ROS 2 and helps keep the content relevant without overcomplicating the core material for beginners.

## 2. ROS 2 Client Libraries

-   **Decision**: Exclusively `rclpy`.
-   **Rationale**: The module's description explicitly highlights "rclpy Python control." Focusing solely on `rclpy` simplifies the module, reduces cognitive load for students (especially those new to ROS 2), and ensures content remains concise, aligning with word count constraints. `rclcpp` can be explored in a more advanced, dedicated module if needed.

## 3. Robot Description Formats

-   **Decision**: Exclusively URDF.
-   **Rationale**: URDF is the primary and most widely used format for describing robot kinematics and dynamics within the ROS ecosystem. Focusing on URDF provides a strong foundational understanding for students. While SDF is crucial for advanced simulation environments like Gazebo, its inclusion would add significant complexity better suited for a dedicated simulation module.

## 4. Example Environment Focus

-   **Decision**: Simulation-first, with considerations for real-robot deployment.
-   **Rationale**: A simulation-first approach is highly practical for AI robotics students, as it allows for learning and experimentation without requiring access to expensive or complex physical hardware. Including considerations for real-robot deployment provides valuable context, highlights potential differences, and prepares students for future challenges when transitioning to physical systems, all without overcomplicating the initial learning process.
