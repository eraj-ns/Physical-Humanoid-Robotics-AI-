--- 
id: 005
title: NPM Start Failed - Invalid Sidebar IDs
stage: red
date: 2025-12-10
surface: agent
model: gemini-1.5-flash-latest
feature: docusaurus-setup
branch: (unknown)
user: (unknown)
command: npm start
labels: ["error", "docusaurus", "sidebar"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
tests:
---

## Prompt

npm start

## Response snapshot

Command: npm start
Directory: Book/
Output: 
> book@0.0.0 start
> docusaurus start

[INFO] Starting the development server...
[WARNING] The `siteConfig.onBrokenMarkdownLinks` config option is deprecated and will be removed in Docusa
urus v4.
Please migrate and move this option to `siteConfig.markdown.hooks.onBrokenMarkdownLinks` instead.
[ERROR] Loading of version failed for version current

[ERROR] Error: Invalid sidebar file at "sidebars.js".
These sidebar document ids do not exist:
- Module1/index
- Module2/ch01-gazebo-physics-and-colli
- Module2/ch02-digital-twin-environment-
- Module2/index
- Module3/01-Introduction-to-AI-Robot-B...
- Module3/02-Isaac-Sim-Simulation
- Module3/03-Isaac-ROS-VSLAM-and-Nav...
- Module3/index
- Module4/ch04-capstone-autonomous-h...

Available document ids are:
- Module1/ch01-ros2-architecture
- Module1/ch02-nodes-topics-services
- Module1/ch03-python-agents-rclpy
- Module1/ch04-urdf-for-humanoids
- Module1/intro
- Module1/module1
- Module2/ch01-gazebo-physics-and-collisions
- Module2/ch02-digital-twin-environment-design
- Module2/intro
- Module2/module2
- Module3/Introduction-to-AI-Robot-Brain
- Module3/Isaac-ROS-VSLAM-and-Nav2-Planning
- Module3/Isaac-Sim-Simulation
- Module3/module3
- Module4/ch01-voice-to-action
- Module4/ch02-llm-cognitive-planning
- Module4/ch03-vision-and-navigation
- Module4/ch04-capstone-autonomous-humanoid
- Module4/intro
- Module4/module4

    at Object.checkSidebarsDocIds (E:\Book_Hackathon_2\Book\node_modules\@docusaurus\plugin-content-docs\l
ib\sidebars\utils.js:245:19)
    at doLoadVersion (E:\Book_Hackathon_2\Book\node_modules\@docusaurus\plugin-content-docs\lib\versions\l
ib\loadVersion.js:102:19)
    at async loadVersion (E:\Book_Hackathon_2\Book\node_modules\@docusaurus\plugin-content-docs\lib\versions\l
ib\loadVersion.js:119:16)
    at async Promise.all (index 0)
    at async Object.loadContent (E:\Book_Hackathon_2\Book\node_modules\@docusaurus\plugin-content-docs\lib
\index.js:152:33)
    at async E:\Book_Hackathon_2\Book\node_modules\@docusaurus\core\lib\server\plugins\plugins.js:40:23   
    at async Promise.all (index 0)
    at async E:\Book_Hackathon_2\Book\node_modules\@docusaurus\core\lib\server\plugins\plugins.js:146:25  
    at async loadSite (E:\Book_Hackathon_2\Book\node_modules\@docusaurus\core\lib\server\site.js:155:45)  
    at async createReloadableSite (E:\Book_Hackathon_2\Book\node_modules\@docusaurus\core\lib\commands\sta
rt\utils.js:62:16)
[INFO] Docusaurus version: 3.9.2
Node version: v24.11.1
Error: (none)
Exit Code: 1
Signal: (none)
Background PIDs: (none)
Process Group PGID: 8816

## Outcome

- ✅ Impact: Docusaurus server failed to start due to invalid sidebar configuration.
- 🧪 Tests: N/A
- 📁 Files: N/A
- 🔁 Next prompts: Debugging `sidebars.js`
- 🧠 Reflection: Captured `npm start` failure and identified the root cause as invalid sidebar document IDs.
