---
id: specs-003-digital-twin-simulation-data-model
---
# Data Model: Textbook Content Structure

This document defines the data model for the textbook content, which is represented as a structured hierarchy of Markdown files.

## 1. Top-Level Structure

The textbook is organized into modules, and each module is a collection of chapters.

- **Textbook**
  - **Module 1**: The Robotic Nervous System (ROS 2)
  - **Module 2**: The Digital Twin (Gazebo & Unity)
  - **Module 3**: The AI-Robot Brain (NVIDIA Isaac)
  - **Module 4**: Vision-Language-Action (VLA)
  - **Capstone Project**: The Autonomous Humanoid

## 2. Module Structure

Each module is a directory containing a set of chapter files.

- **Module Directory (`/docs/<module-name>/`)**
  - `_category_.json`: Docusaurus file to define the module's sidebar label and position.
  - `ch01-<chapter-title>.md`: Markdown file for the first chapter.
  - `ch02-<chapter-title>.md`: Markdown file for the second chapter.
  - ... and so on.

## 3. Chapter Structure (`.md` file)

Each chapter is a Markdown file with a consistent structure.

- **Front Matter**: YAML metadata at the top of the file.
  - `id`: A unique identifier for the chapter.
  - `title`: The full title of the chapter.
  - `description`: A brief summary of the chapter's content.
  - `tags`: A list of keywords related to the chapter.
- **Chapter Content**:
  - **Learning Objectives**: A bulleted list of what the reader will be able to do after completing the chapter.
  - **Introduction**: A brief overview of the chapter's topics.
  - **Main Content Sections**: The body of the chapter, divided into logical sections with H2 and H3 headings.
  - **Code Examples**: Runnable code snippets with explanations.
  - **Interactive Examples (Future)**: Embedded React components for interactive learning experiences.
  - **Conclusion**: A summary of the key takeaways.
  - **References**: A list of all cited sources in APA 7th edition format.

## 4. Entity Relationship Diagram (Conceptual)

This diagram illustrates the conceptual relationship between the different content entities.

```mermaid
graph TD;
    A[Textbook] --> B1[Module 1];
    A --> B2[Module 2];
    A --> B3[Module 3];
    A --> B4[Module 4];
    A --> B5[Capstone];

    B2 --> C1[Chapter 1: Gazebo Physics];
    B2 --> C2[Chapter 2: Environment Design];
    B2 --> C3[Chapter 3: Unity Visualization];
    B2 --> C4[Chapter 4: Sensor Simulation];

    C1 --> D1[Learning Objectives];
    C1 --> D2[Introduction];
    C1 --> D3[Main Content];
    C1 --> D4[Code Examples];
    C1 --> D5[Conclusion];
    C1 --> D6[References];
```
