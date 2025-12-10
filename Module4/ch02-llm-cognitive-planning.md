# Chapter 2: LLM Cognitive Planning (ROS 2)

In the previous chapter, we learned how to convert voice commands into text. Now, we'll take that text and use a Large Language Model (LLM) to create a high-level plan for our robot. This is where the "cognitive" part of our AI-Robot Brain comes into play.

## Introduction to LLMs for Planning

LLMs are incredibly powerful tools for understanding and generating human-like text. We can leverage this power to translate a user's natural language command into a sequence of actions that a robot can execute. For example, if a user says "go to the kitchen and get the apple", the LLM can break this down into a plan like:
1.  Navigate to the kitchen.
2.  Find the apple.
3.  Pick up the apple.

### Designing Prompts for Robot Tasks

The key to getting a good plan from an LLM is to design a good prompt. The prompt should provide the LLM with enough context to understand the robot's capabilities and the current state of the world.

Here's an example of a prompt we could use:

```
You are a helpful robot assistant. Your task is to take a user's command and break it down into a simple, step-by-step plan that you can execute.

You can perform the following actions:
- navigate_to(location)
- find_object(object_name)
- pick_up(object_name)
- put_down(object_name)

The user's command is: "{command}"

Your plan should be a numbered list of actions.
```

## Integrating an LLM with ROS 2

Now, let's create a ROS 2 node that subscribes to the `/voice_commands` topic, sends the command to an LLM, and publishes the resulting plan.

Create a new file `voice_commander/planner_node.py` with the following content:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai

class PlannerNode(Node):
    def __init__(self):
        super().__init__('planner_node')
        self.subscription = self.create_subscription(
            String,
            'voice_commands',
            self.command_callback,
            10)
        self.plan_publisher_ = self.create_publisher(String, 'robot_plan', 10)
        
        # NOTE: You will need to have your OpenAI API key set as an environment variable
        # export OPENAI_API_KEY='your-api-key'
        self.openai_client = openai.OpenAI()

        self.get_logger().info("Planner node started.")

    def command_callback(self, msg):
        command = msg.data
        self.get_logger().info(f"Received command: '{command}'")
        
        prompt = f"""
        You are a helpful robot assistant. Your task is to take a user's command and break it down into a simple, step-by-step plan that you can execute.

        You can perform the following actions:
        - navigate_to(location)
        - find_object(object_name)
        - pick_up(object_name)
        - put_down(object_name)

        The user's command is: "{command}"

        Your plan should be a numbered list of actions.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            
            plan = response.choices[0].message.content
            self.get_logger().info(f"Generated plan:\n{plan}")
            
            plan_msg = String()
            plan_msg.data = plan
            self.plan_publisher_.publish(plan_msg)

        except Exception as e:
            self.get_logger().error(f"Error generating plan: {e}")


def main(args=None):
    rclpy.init(args=args)
    planner_node = PlannerNode()
    rclpy.spin(planner_node)
    planner_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This node listens for commands on the `/voice_commands` topic. When it receives a command, it constructs a prompt and sends it to the OpenAI API. The LLM's response, which is the plan, is then published to the `/robot_plan` topic.

In the next chapter, we'll look at how to execute this plan and use the robot's vision system to navigate and interact with the world.