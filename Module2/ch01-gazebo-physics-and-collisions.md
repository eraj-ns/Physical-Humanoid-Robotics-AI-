---
id: ch01-gazebo-physics-and-collisions
title: "Chapter 1: Gazebo Physics & Collisions"
description: "An introduction to physics and collision modeling in Gazebo."
tags: ["gazebo", "physics", "collisions", "ros2", "sdf", "urdf"]
---

## Learning Objectives

- Explain the role of physics engines in robotics simulation.
- Configure global physics properties in a Gazebo world.
- Define material properties and apply them to models.
- Create and validate collision geometries for a robot model.

## Introduction

Welcome to the exciting world of robotics simulation! A key aspect of creating realistic and useful simulations is the accurate modeling of physics and collisions. In this chapter, you will learn the fundamentals of how Gazebo handles physics and how you can configure it to create high-fidelity simulations for your robots.

## Gazebo's Physics Engines

Gazebo is a powerful and flexible simulator that supports multiple physics engines. A physics engine is the software component that simulates the laws of physics, such as gravity, friction, and forces. The choice of physics engine can have a significant impact on the accuracy and performance of your simulation.

Gazebo supports the following physics engines:

- **ODE (Open Dynamics Engine)**: The default physics engine in Gazebo. It is a mature and widely used engine, known for its speed and stability.
- **Bullet**: A popular open-source physics engine, known for its performance and support for a wide range of features.
- **Simbody**: A high-performance, high-accuracy physics engine, often used for biomechanical and complex multibody systems.
- **DART (Dynamic Animation and Robotics Toolkit)**: A flexible and extensible physics engine, designed for robotics and animation.

You can select the physics engine in your Gazebo world file (`.world`). For most applications, the default ODE engine is a good choice.

## Configuring Global Physics Properties

The global physics properties for a Gazebo world are defined within the `<physics>` block in the world file. This allows you to control the overall behavior of the simulation.

Here's an example of a `<physics>` block:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>
  <gravity>0 0 -9.8</gravity>
</physics>
```

- **`type`**: Specifies the physics engine to use (e.g., "ode").
- **`max_step_size`**: The maximum time step for the physics simulation. A smaller value will result in a more accurate but slower simulation.
- **`real_time_factor`**: A factor to control the speed of the simulation relative to real time. A value of 1 means the simulation runs at real time.
- **`real_time_update_rate`**: The rate at which the simulation is updated.
- **`gravity`**: The gravity vector for the simulation.

## Material Properties

In addition to global physics properties, you can also define material properties for individual objects in your simulation. This allows you to control how objects interact with each other.

Material properties are defined within the `<surface>` block of a `<collision>` element in an SDF or URDF file.

```xml
<collision name="collision">
  <geometry>
    <box>
      <size>1 1 1</size>
    </box>
  </geometry>
  <surface>
    <friction>
      <ode>
        <mu>0.8</mu>
        <mu2>0.8</mu2>
      </ode>
    </friction>
    <contact>
      <ode>
        <kp>1e+13</kp>
        <kd>1</kd>
      </ode>
    </contact>
  </surface>
</collision>
```

- **`<friction>`**: Defines the friction properties of the surface. `mu` and `mu2` are the primary and secondary friction coefficients.
- **`<contact>`**: Defines the contact properties of the surface. `kp` and `kd` are the stiffness and damping of the contact.

## Collision Modeling

Accurate collision modeling is crucial for realistic simulations. In Gazebo, collision geometries are defined within the `<collision>` element of a link in an SDF or URDF file.

You can use primitive shapes (box, cylinder, sphere) for simple collision geometries, or you can use mesh files for more complex shapes.

```xml
<collision name="collision">
  <geometry>
    <mesh>
      <uri>model://my_robot/meshes/my_collision_mesh.dae</uri>
    </mesh>
  </geometry>
</collision>
```

It is a good practice to use simpler collision geometries than the visual geometries, as this can significantly improve the performance of the simulation.

## Conclusion

In this chapter, you have learned the basics of physics and collision modeling in Gazebo. You now have the knowledge to configure the physics properties of your simulations and create accurate collision models for your robots. In the next chapter, we will build upon this knowledge to design a complete digital twin environment.

## References

- [Gazebo Physics Documentation](http://gazebosim.org/tutorials?tut=physics_params)
- [SDF Format Documentation](http://sdformat.org/spec)
