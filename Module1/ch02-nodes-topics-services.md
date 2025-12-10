# Chapter 2: Nodes, Topics, Services

In Chapter 1, we introduced the fundamental concepts of ROS 2 and its architectural overview. Now, we'll dive deeper into the core communication mechanisms that allow different parts of your robot's software to interact: Nodes, Topics, and Services. Understanding these paradigms is crucial for building any non-trivial ROS 2 application.

## Introduction to Communication Patterns

ROS 2 provides several distinct communication patterns, each suited for different use cases. The three primary patterns are:

1.  **Topics**: For asynchronous, one-way streaming of data (like sensor readings or motor commands).
2.  **Services**: For synchronous, request-response interactions (like triggering an action and waiting for a result).
3.  **Actions**: For long-running, goal-oriented tasks that provide continuous feedback. (We'll introduce Actions briefly here and explore them more in later modules if needed).

## Nodes in Detail

As established, a node is a process that performs computation. In practice, a ROS 2 system is a collection of nodes working together.

### Creating and Launching Nodes

Nodes are typically created within ROS 2 packages. A simple Python node written with `rclpy` (which we'll cover in detail in Chapter 3) might look like this:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        self.get_logger().info('My node has started!')

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node) # Keeps the node alive until Ctrl+C is pressed
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

To run this node after building its package, you would typically use `ros2 run`:

```bash
ros2 run <package_name> <executable_name>
```

### Node Lifecycle

ROS 2 introduces a managed node lifecycle, particularly for long-running and critical applications. This lifecycle allows nodes to explicitly transition through states (e.g., `unconfigured`, `inactive`, `active`, `finalized`), enabling more robust error handling and controlled startup/shutdown sequences. For simple nodes, you often interact with a default lifecycle, but for advanced systems, understanding this is key.

## Topics for Asynchronous Communication

Topics are the most common way for nodes to exchange data. They are designed for data streams where multiple producers (publishers) can send data to multiple consumers (subscribers) without needing direct knowledge of each other.

### Publishers and Subscribers: How They Work

-   **Publisher**: A node that sends messages to a specific topic.
-   **Subscriber**: A node that listens for messages on a specific topic.

When a publisher sends a message to a topic, all nodes subscribed to that topic will receive a copy of the message. This is a "fire-and-forget" mechanism; the publisher doesn't wait for confirmation of receipt.

### Message Types

Data transmitted over topics are strongly typed. This means every message has a predefined structure, ensuring consistency. ROS 2 provides a set of standard message types (e.g., `std_msgs/msg/String`, `geometry_msgs/msg/Twist` for robot velocities, `sensor_msgs/msg/Image` for camera data). You can also define custom message types for application-specific data.

### `ros2 topic` Commands

The `ros2 topic` command-line tool is indispensable for inspecting and interacting with topics:

-   `ros2 topic list`: Lists all currently active topics.
-   `ros2 topic info <topic_name>`: Shows information about a specific topic, including its type and the nodes publishing/subscribing to it.
-   `ros2 topic echo <topic_name>`: Displays messages being published to a topic in real-time.
-   `ros2 topic pub <topic_name> <msg_type> <args>`: Publishes a single message to a topic from the command line.

**Example**: Publishing a simple string message:
```bash
ros2 topic pub /my_topic std_msgs/msg/String '{data: "Hello ROS 2"}'
```

## Services for Synchronous Communication

Services are used when you need a direct request-response interaction between two nodes. Unlike topics, where messages flow continuously, a service is invoked, and the client typically waits for the server to process the request and send back a response.

### Clients and Servers: Request/Response Model

-   **Service Server**: A node that provides a service. It waits for incoming requests, processes them, and sends back a response.
-   **Service Client**: A node that requests a service from a service server and waits for the response.

Services are ideal for actions that have a clear start and end, such as "get current robot position" or "toggle a gripper".

### Service Types

Similar to messages, services also have predefined types. A service type defines both the structure of the request message and the structure of the response message.

### `ros2 service` Commands

The `ros2 service` command-line tool helps with service inspection and invocation:

-   `ros2 service list`: Lists all currently available services.
-   `ros2 service type <service_name>`: Shows the type of a specific service.
-   `ros2 service call <service_name> <service_type> <request_args>`: Calls a service from the command line with a given request.

**Example**: Calling a service to add two integers (assuming an `example_interfaces/srv/AddTwoInts` service type):
```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"
```

## Actions for Long-Running Tasks (Brief Introduction)

Actions extend the service concept for long-running tasks that can be preempted and provide periodic feedback. They are particularly useful for tasks like navigating to a goal, where you might want to know the robot's progress and potentially cancel the operation.

An Action consists of:
-   A **Goal**: The objective the client wants the server to achieve.
-   **Feedback**: Continuous updates on the progress of the goal.
-   A **Result**: The final outcome of the goal once completed.

While implementing actions is more complex, ROS 2 provides `ros2 action` commands for basic interaction:
-   `ros2 action list`: Lists available actions.
-   `ros2 action send_goal`: Sends a goal to an action server from the command line.

## Chapter Summary

This chapter provided a detailed exploration of ROS 2's core communication patterns: Nodes, Topics, Services, and a brief introduction to Actions. You learned how they function, their use cases, and how to interact with them using ROS 2 command-line tools. In the next chapter, we will bring these concepts to life by writing actual ROS 2 nodes in Python using the `rclpy` client library.