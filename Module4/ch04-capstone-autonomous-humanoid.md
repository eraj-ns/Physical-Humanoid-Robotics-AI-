# Chapter 4: Capstone: The Autonomous Humanoid

Welcome to the capstone project for the Vision-Language-Action module! In this chapter, we will integrate all the components we've built in the previous chapters to create an autonomous humanoid robot that can understand voice commands, create a plan, and execute it in a simulated environment.

## Project Overview

The goal of this project is to create a complete end-to-end VLA pipeline. Here's how it will work:

1.  **Voice Command**: The user will give a voice command to the robot, like "go to the table and pick up the red cube".
2.  **Speech-to-Text**: The `voice_node` will capture the audio, use Whisper to transcribe it into text, and publish it to the `/voice_commands` topic.
3.  **LLM Planning**: The `planner_node` will receive the text command, use an LLM to generate a step-by-step plan, and publish the plan to the `/robot_plan` topic.
4.  **Execution Engine**: A new node, the `executor_node`, will subscribe to the `/robot_plan` topic and execute each step of the plan. This node will be the "brains" of the robot, coordinating its actions.
5.  **Navigation and Vision**: For actions like `navigate_to(location)` and `find_object(object_name)`, the `executor_node` will use Nav2 and our object detection capabilities to move the robot and perceive its environment.
6.  **Manipulation**: For actions like `pick_up(object_name)`, the `executor_node` will control the robot's arm and gripper.

## Step-by-Step Guide

### 1. The Executor Node

The `executor_node` is the central piece of this project. It will need to:
- Subscribe to the `/robot_plan` topic.
- Parse the plan into a sequence of actions.
- For each action, call the appropriate service or action server. For example:
    - For `navigate_to(location)`, it would call a Nav2 action server.
    - For `find_object(object_name)`, it would call a service that uses our computer vision node.
    - For `pick_up(object_name)`, it would control the robot's arm.

Here is a skeleton for the `executor_node.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ExecutorNode(Node):
    def __init__(self):
        super().__init__('executor_node')
        self.subscription = self.create_subscription(
            String,
            'robot_plan',
            self.plan_callback,
            10)
        self.get_logger().info("Executor node started.")

    def plan_callback(self, msg):
        plan = msg.data.split('\n')
        self.get_logger().info(f"Executing plan:\n{msg.data}")
        
        for step in plan:
            if not step.strip():
                continue
            
            self.execute_step(step)

    def execute_step(self, step):
        self.get_logger().info(f"Executing step: {step}")
        # Here you would parse the step and call the appropriate
        # ROS 2 action or service.
        # For example, if step is "navigate_to(kitchen)":
        #   self.call_nav2_action_server("kitchen")

def main(args=None):
    rclpy.init(args=args)
    executor_node = ExecutorNode()
    rclpy.spin(executor_node)
    executor_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2. Integrating Nav2 for Navigation

To use Nav2, you will need to have it installed and configured for your robot. This is a complex topic that is beyond the scope of this introductory module, but you can find excellent tutorials on the official Nav2 website.

Once configured, you can use a ROS 2 action client in your `executor_node` to send navigation goals to Nav2.

### 3. Final Demonstration

Once all the pieces are in place, you should be able to run all your nodes and see the robot perform a complete task based on a voice command.

1.  Launch your simulation environment with the robot.
2.  Run the `voice_node`, `planner_node`, and `executor_node`.
3.  Give a voice command, like "go to the desk and find the book".
4.  Watch as the robot navigates to the desk and looks for the book.

Congratulations! You have built a complete Vision-Language-Action pipeline for an autonomous humanoid robot. This is a huge achievement and a testament to the power of modern AI and robotics.