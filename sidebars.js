/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: ROS 2 Architecture & Programming',
      // Docusaurus automatically uses the directory name (Module1) if 'link' is omitted,
      // but 'index.md' or 'intro.md' can serve as the main landing page.
      // Hum 'intro.md' ko pehla item bana dete hain.
      
      items: [
        'Module1/intro', 
        'Module1/index', 
        'Module1/ch01-ros2-architecture',
        'Module1/ch02-nodes-topics-services',
        'Module1/ch03-python-agents-rclpy',
        'Module1/ch04-urdf-for-humanoids',
      ],
    },
    
    {
      type: 'category',
      label: 'Module 2: Digital Twin and Simulation',
      items: [
        'Module2/intro',
        'Module2/index',
        'Module2/ch01-gazebo-physics-and-colli', // .md extension ke baghair ch01-gazebo-physics-and-colli
        'Module2/ch02-digital-twin-environment-', // .md extension ke baghair ch02-digital-twin-environment-
      ],
    },
    
    {
      type: 'category',
      label: 'Module 3: Isaac Sim and AI-Robot Basics',
      items: [
        'Module3/01-Introduction-to-AI-Robot-B...', // .md extension ke baghair 01-Introduction-to-AI-Robot-B...
        'Module3/02-Isaac-Sim-Simulation',
        'Module3/03-Isaac-ROS-VSLAM-and-Nav...',
        'Module3/index',
      ],
    },
    
    {
      type: 'category',
      label: 'Module 4: Cognitive Planning and Autonomy',
      // Aapki image mein '_category_json' file hai, lekin Docusaurus ko uski zaroorat nahi hoti.
      items: [
        'Module4/ch01-voice-to-action',
        'Module4/ch02-llm-cognitive-planning',
        'Module4/ch03-vision-and-navigation',
        'Module4/ch04-capstone-autonomous-h...',
      ],
    },
  ],
};

module.exports = sidebars;