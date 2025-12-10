# Chapter 3: Vision & Navigation

With a plan in hand, our robot now needs to execute it. This is where vision and navigation come into play. In this chapter, we'll explore how a robot can use its camera to "see" the world and navigate through it.

## Introduction to Computer Vision in ROS

Computer vision is a field of artificial intelligence that enables computers to interpret and understand the visual world. In ROS 2, computer vision is typically handled by nodes that process image data from a camera and publish the results.

The most common message type for image data in ROS 2 is `sensor_msgs/msg/Image`. A camera driver will publish `Image` messages to a topic, and computer vision nodes will subscribe to that topic.

### Using a Simulated Camera

In our simulation environment, we can add a camera sensor to our robot model. This simulated camera will publish `Image` messages, just like a real camera would. This allows us to develop and test our computer vision code without needing a physical robot.

In Gazebo, you can add a camera sensor to your robot's URDF file like this:

```xml
<gazebo reference="camera_link">
  <sensor type="camera" name="camera">
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>800</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <namespace>/demo</namespace>
        <remapping>image_raw:=image_raw</remapping>
        <remapping>camera_info:=camera_info</remapping>
      </ros>
    </plugin>
  </sensor>
</gazebo>
```

This XML snippet defines a camera sensor and uses a plugin to publish the camera's images and info to ROS 2 topics.

## Basic Object Detection and Navigation

For our VLA module, the robot needs to be able to find objects. A simple way to do this is to use a pre-trained object detection model. These models can take an image as input and output a list of objects and their locations in the image.

Here's a conceptual example of a ROS 2 node that could perform object detection:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.subscription = self.create_subscription(
            Image,
            '/demo/image_raw',
            self.image_callback,
            10)
        self.bridge = CvBridge()
        # In a real implementation, you would load your object detection model here
        # self.model = load_my_model()

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Here you would run your object detection model on the cv_image
        # detections = self.model.detect(cv_image)
        
        # For this example, we'll just draw a rectangle
        cv2.rectangle(cv_image, (100, 100), (200, 200), (0, 255, 0), 2)
        
        cv2.imshow("Object Detection", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    object_detector = ObjectDetector()
    rclpy.spin(object_detector)
    object_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This node subscribes to the camera's image topic, converts the ROS `Image` message to an OpenCV image, and then (in a real implementation) would run an object detection model.

For navigation, ROS 2 provides the powerful Navigation2 stack (Nav2). Nav2 can take a goal location and generate a path for the robot to follow, while avoiding obstacles. Integrating Nav2 is a more advanced topic that we will cover in the capstone project.

In the final chapter, we'll bring everything together to create our autonomous humanoid.