# Chapter 1: Voice-to-Action (Whisper)

Welcome to the first chapter of Module 4! In this chapter, we'll dive into the exciting world of voice-controlled robotics. You'll learn how to capture spoken commands and turn them into actionable data that a robot can understand. We'll be using OpenAI's Whisper for speech-to-text conversion and integrating it into a ROS 2 ecosystem.

## Introduction to Speech-to-Text

Speech-to-text, also known as automatic speech recognition (ASR), is a technology that converts spoken language into written text. In robotics, ASR is a key component for creating natural and intuitive human-robot interfaces. Instead of using a keyboard or a joystick, you can simply tell the robot what to do.

### Why Whisper?

OpenAI's Whisper is a state-of-the-art ASR system that is trained on a large and diverse dataset of audio. It is highly accurate, robust to background noise, and can handle a wide variety of accents and languages. These features make it an excellent choice for robotics applications where reliability is crucial.

## Setting up Whisper

To get started with Whisper, you'll need to install the `openai-whisper` package.

```bash
pip install openai-whisper
```

You'll also need to have `ffmpeg` installed on your system.

```bash
# on Ubuntu
sudo apt update && sudo apt install ffmpeg
```

Once installed, you can use Whisper to transcribe an audio file with just a few lines of Python code:

```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("path/to/audio.mp3")
print(result["text"])
```

## Creating a ROS 2 Node for Voice Commands

Now that we know how to use Whisper, let's create a ROS 2 node that listens to a microphone, transcribes the audio, and publishes the text to a topic.

First, you'll need to create a new ROS 2 package.

```bash
ros2 pkg create --build-type ament_python voice_commander
```

Inside the `voice_commander` package, create a new file `voice_commander/voice_node.py` with the following content:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import speech_recognition as sr
import whisper

class VoiceNode(Node):
    def __init__(self):
        super().__init__('voice_node')
        self.publisher_ = self.create_publisher(String, 'voice_commands', 10)
        self.recognizer = sr.Recognizer()
        self.whisper_model = whisper.load_model("base")

        self.get_logger().info("Listening for voice commands...")
        self.listen()

    def listen(self):
        with sr.Microphone() as source:
            while rclpy.ok():
                try:
                    audio = self.recognizer.listen(source)
                    with open("temp_audio.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    
                    result = self.whisper_model.transcribe("temp_audio.wav")
                    command_text = result["text"]
                    
                    if command_text:
                        self.get_logger().info(f"Heard: {command_text}")
                        msg = String()
                        msg.data = command_text
                        self.publisher_.publish(msg)
                except sr.UnknownValueError:
                    self.get_logger().warning("Could not understand audio")
                except sr.RequestError as e:
                    self.get_logger().error(f"Could not request results; {e}")

def main(args=None):
    rclpy.init(args=args)
    voice_node = VoiceNode()
    rclpy.spin(voice_node)
    voice_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This node uses the `speech_recognition` library to capture audio from the microphone and then uses Whisper to transcribe it. The transcribed text is then published to the `/voice_commands` topic.

In the next chapter, we'll see how to use an LLM to process these commands and generate a plan for the robot.