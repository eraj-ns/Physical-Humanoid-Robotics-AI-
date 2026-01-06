# Chapter 3: Python Agents via `rclpy`

In the previous chapters, we gained a solid understanding of ROS 2's architecture and its core communication paradigms. Now, it's time to put that knowledge into practice by writing our own ROS 2 nodes in Python using the `rclpy` client library. Python, with its readability and vast ecosystem of libraries, is an excellent choice for rapid prototyping and developing control logic in ROS 2.

## Introduction to `rclpy`

`rclpy` is the official Python client library for ROS 2. It provides a Pythonic interface to the underlying ROS 2 C API (`rcl`), allowing developers to easily create nodes, publishers, subscribers, service clients, and service servers in Python.

### Why Python for ROS 2?

-   **Rapid Prototyping**: Python's dynamic nature and simplified syntax allow for quick development and testing of ideas.
-   **Ease of Use**: It's generally easier to learn and write Python code compared to C++, making it accessible for beginners and efficient for complex scripting tasks.
-   **Rich Ecosystem**: Python boasts a massive collection of scientific computing, AI, and data processing libraries that can be easily integrated into ROS 2 applications.

### `rclpy` vs `rclcpp` (Reiterate `rclpy` focus)

While `rclcpp` (the C++ client library) offers performance benefits crucial for highly demanding tasks like real-time sensor processing and low-level motor control, `rclpy` is perfectly suitable and often preferred for higher-level control, logic, and rapid application development. This module will exclusively focus on `rclpy` to maintain a clear learning path and leverage Python's strengths.

## Creating a Simple `rclpy` Node

Every ROS 2 application starts with a node. Here's the basic structure of an `rclpy` node:

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # Node initialization goes here
        self.get_logger().info('Hello, ROS 2 from a Python node!')

def main(args=None):
    rclpy.init(args=args)  # Initialize the ROS 2 client library
    minimal_publisher = MinimalPublisher() # Create an instance of our node
    rclpy.spin(minimal_publisher) # Keep the node alive until manually stopped
    minimal_publisher.destroy_node() # Destroy the node explicitly
    rclpy.shutdown() # Shutdown the ROS 2 client library

if __name__ == '__main__':
    main()
```

### Initializing and Shutting Down ROS 2

-   `rclpy.init(args=args)`: This function initializes the ROS 2 client library. It must be called before any other `rclpy` functions. The `args` argument allows passing command-line arguments to the ROS 2 system.
-   `rclpy.spin(node)`: This function prevents the node from exiting immediately. It keeps the node alive, processing callbacks (e.g., from subscribers or timers) until `rclpy.shutdown()` is called or `Ctrl+C` is pressed.
-   `node.destroy_node()`: Explicitly destroys the node, releasing all associated resources. Good practice for cleanup.
-   `rclpy.shutdown()`: Shuts down the ROS 2 client library, releasing all resources and communication channels.

## Publishing Data with `rclpy`

Let's create a node that periodically publishes a "Hello ROS 2" message to a topic.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Import the message type

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # Create a publisher to the 'topic' topic, of type String, with a queue size of 10
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.i = 0
        # Create a timer that calls the timer_callback function every 0.5 seconds
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info('Minimal Publisher node has started!')

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2: {self.i}'
        self.publisher_.publish(msg) # Publish the message
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

To run this:
1.  Save the code as `minimal_publisher.py` in your ROS 2 package (e.g., `my_ros2_pkg/my_ros2_pkg/minimal_publisher.py`).
2.  Add an entry point in `setup.py` of your package:
    ```python
    entry_points={
        'console_scripts': [
            'minimal_publisher = my_ros2_pkg.minimal_publisher:main',
        ],
    },
    ```
3.  Build your package: `colcon build --packages-select my_ros2_pkg`
4.  Source your `install` directory: `source install/setup.bash` (or `.ps1` for Windows)
5.  Run the node: `ros2 run my_ros2_pkg minimal_publisher`

You can then see the messages using `ros2 topic echo /topic`.

## Subscribing to Data with `rclpy`

Now, let's create a node that subscribes to the topic and prints the received messages.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        # Create a subscriber to the 'topic' topic, of type String
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning
        self.get_logger().info('Minimal Subscriber node has started!')

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

To run this:
1.  Save as `minimal_subscriber.py` in your package.
2.  Add an entry point in `setup.py`:
    ```python
    entry_points={
        'console_scripts': [
            'minimal_publisher = my_ros2_pkg.minimal_publisher:main',
            'minimal_subscriber = my_ros2_pkg.minimal_subscriber:main', # New entry
        ],
    },
    ```
3.  Build and source.
4.  Run the subscriber: `ros2 run my_ros2_pkg minimal_subscriber`
5.  Run the publisher in another terminal: `ros2 run my_ros2_pkg minimal_publisher`

You should see the subscriber printing the messages from the publisher.

## Implementing a Simple Service/Client

Services provide a request-response mechanism. Let's create a simple service to add two integers.

### Service Server Implementation

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # Import the service type

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        # Create a service of type AddTwoInts on the 'add_two_ints' service name
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('Add Two Ints Service has started!')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}')
        self.get_logger().info(f'Sending back response: {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    minimal_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Client Implementation

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import sys

class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        # Create a service client for the 'add_two_ints' service
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req) # Send the request asynchronously

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    
    # Get arguments from command line
    if len(sys.argv) == 3:
        minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    else:
        minimal_client.get_logger().error('Usage: ros2 run <pkg_name> minimal_client_async <a> <b>')
        minimal_client.destroy_node()
        rclpy.shutdown()
        return

    while rclpy.ok():
        rclpy.spin_once(minimal_client)
        if minimal_client.future.done():
            try:
                response = minimal_client.future.result()
            except Exception as e:
                minimal_client.get_logger().error(f'Service call failed: {e}')
            else:
                minimal_client.get_logger().info(
                    f'Result of add_two_ints: {minimal_client.req.a} + {minimal_client.req.b} = {response.sum}')
            break
    
    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

To run this:
1.  Save the service code as `minimal_service.py` and client code as `minimal_client_async.py` in your package.
2.  Add entry points in `setup.py`.
3.  Build and source.
4.  Run the service: `ros2 run my_ros2_pkg minimal_service`
5.  Run the client in another terminal: `ros2 run my_ros2_pkg minimal_client_async 5 3`

## Building and Running `rclpy` Packages

As seen in the examples, building ROS 2 packages uses `colcon`, a build system.
-   `colcon build`: Builds all packages in your workspace.
-   `colcon build --packages-select <pkg_name>`: Builds a specific package.
-   After building, always `source install/setup.bash` (or equivalent) to set up your environment variables.

Then, you can run your nodes using `ros2 run <package_name> <executable_name>`.

## Chapter Summary

This chapter walked you through the process of creating functional ROS 2 nodes using `rclpy` in Python. You learned how to implement publishers, subscribers, service servers, and service clients. With these skills, you can now start building more complex robot behaviors and communication flows. In the next chapter, we will shift our focus to representing the physical structure of our robot using URDF.