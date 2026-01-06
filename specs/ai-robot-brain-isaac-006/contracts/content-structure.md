---
id: specs-006-ai-robot-brain-isaac-contracts-content-structure
---
# Contract: Content Structure

This document defines the content structure for Module 3. All generated content must adhere to this structure.

## Directory Structure

The module's content will reside within the `Book/docs/Module3/` directory.

```
Book/
└── docs/
    └── Module3/
        ├── 01-Introduction-to-AI-Robot-Brain.md
        ├── 02-Isaac-Sim-Simulation.md
        ├── 03-Isaac-ROS-VSLAM.md
        ├── 04-Nav2-Path-Planning.md
        └── assets/
            └── ... (images, diagrams, etc.)
```

## File Naming

-   Chapter files MUST be prefixed with a two-digit number (e.g., `01-`, `02-`) to ensure proper ordering.
-   File names should be descriptive and use kebab-case (e.g., `Introduction-to-AI-Robot-Brain.md`).

## Chapter Content (`.md` files)

Each Markdown file representing a chapter MUST include:

1.  **Title**: A main `<h1>` title that matches the chapter's topic.
2.  **Introduction**: A brief paragraph summarizing the chapter's learning objectives.
3.  **Body Content**: The main instructional text, code blocks, images, and other Docusaurus components.
4.  **Code Blocks**: All code examples MUST be in properly formatted code blocks with the correct language specified (e.g., `python`, `bash`, `xml`).
5.  **References**: If external sources are used, a "References" section with APA-style citations MUST be included at the end of the chapter.

## Sidebar Navigation

The `Book/sidebars.js` file will be updated to include an entry for Module 3, with links to each chapter in the correct order. Example structure:

```javascript
// In sidebars.js
{
  type: 'category',
  label: 'Module 3: The AI-Robot Brain',
  items: [
    'Module3/01-Introduction-to-AI-Robot-Brain',
    'Module3/02-Isaac-Sim-Simulation',
    'Module3/03-Isaac-ROS-VSLAM',
    'Module3/04-Nav2-Path-Planning',
  ],
}
```
