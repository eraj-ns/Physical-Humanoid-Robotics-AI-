/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [

    // ---------- MODULE 1 ----------
    {
      type: 'category',
      label: 'Module 1: ROS 2 Architecture & Programming',
      items: [
        'Module1/intro',
        'Module1/ch01-ros2-architecture',
        'Module1/ch02-nodes-topics-services',
        'Module1/ch03-python-agents-rclpy',
        'Module1/ch04-urdf-for-humanoids',
        'Module1/module1',
      ],
    },

    // ---------- MODULE 2 ----------
    {
      type: 'category',
      label: 'Module 2: Digital Twin and Simulation',
      items: [
        'Module2/intro',
        'Module2/ch01-gazebo-physics-and-collisions',
        'Module2/ch02-digital-twin-environment-design',
        'Module2/module2',
      ],
    },

    // ---------- MODULE 3 ----------
    {
      type: 'category',
      label: 'Module 3: Isaac Sim and AI-Robot Basics',
      items: [
        'Module3/Introduction-to-AI-Robot-Brain',
        'Module3/Isaac-Sim-Simulation',
        'Module3/Isaac-ROS-VSLAM-and-Nav2-Planning',
        'Module3/module3',
      ],
    },

    // ---------- MODULE 4 ----------
    {
      type: 'category',
      label: 'Module 4: Cognitive Planning and Autonomy',
      items: [
        'Module4/intro',
        'Module4/ch01-voice-to-action',
        'Module4/ch02-llm-cognitive-planning',
        'Module4/ch03-vision-and-navigation',
        'Module4/ch04-capstone-autonomous-humanoid',
      ],
    },

  ],
};

module.exports = sidebars;
