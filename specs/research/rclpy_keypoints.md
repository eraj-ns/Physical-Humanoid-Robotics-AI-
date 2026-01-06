# rclpy Programming: Key Points

This document synthesizes the key programming concepts for `rclpy`.

## 1. Node Creation

A `rclpy` node is typically a Python class that inherits from `rclpy.node.Node`.

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
```

## 2. Publishers and Subscribers

Publishers and subscribers are created using the `create_publisher` and `create_subscription` methods of the `Node` class.

```python
from std_msgs.msg import String

# ... inside a Node class ...
self.publisher_ = self.create_publisher(String, 'topic', 10)
self.subscription = self.create_subscription(
    String,
    'topic',
    self.listener_callback,
    10)
```

## 3. Timers

Timers are used to trigger a callback at a regular interval.

```python
# ... inside a Node class ...
timer_period = 0.5  # seconds
self.timer = self.create_timer(timer_period, self.timer_callback)
```

## 4. Executors

An executor is used to spin nodes, allowing their callbacks to be executed. The `spin` function is a blocking call.

```python
rclpy.init(args=args)
node = MyNode()
rclpy.spin(node)
rclpy.shutdown()
```
