---
id: specs-006-ai-robot-brain-isaac-research
---
# Research: Module 3 Planning

This document outlines the research findings for planning Module 3: The AI-Robot Brain.

## 1. Docusaurus Features

**Decision**: We will leverage the following Docusaurus features:
- **MDX**: To allow for interactive components within the documentation, such as code block copy buttons and potentially simple simulations or quizzes later.
- **Admonitions**: To highlight notes, tips, and warnings (e.g., hardware requirements).
- **Tabs**: To switch between different code examples (e.g., Python vs. shell commands) or to show different perspectives.
- **Content Versioning**: While not immediately required for this module, being aware of this feature is important for future editions of the textbook.

**Rationale**: These features enhance the readability and interactivity of the content, which is crucial for a technical textbook aimed at students.

**Alternatives considered**: Plain Markdown. Rejected because it lacks the rich interactive features of MDX.

## 2. Chapter Organization

**Decision**: The chapters will be organized sequentially within the `Book/docs/Module3` directory, prefixed with numbers to enforce order. The `sidebars.js` file will be updated to reflect this structure.

```
Book/docs/Module3/
├── 01-Introduction-to-AI-Robot-Brain.md
├── 02-Isaac-Sim-Simulation.md
├── 03-Isaac-ROS-VSLAM.md
├── 04-Nav2-Path-Planning.md
└── assets/
```

**Rationale**: A flat, numbered structure is simple, easy to navigate, and clearly communicates the intended progression through the material.

**Alternatives considered**: A nested structure with sub-directories for each chapter. Rejected as overly complex for the number of chapters in this module.

## 3. Citation Management

**Decision**: Citations will be managed manually using APA style, with a dedicated "References" section at the end of each chapter.

**Rationale**: For the scope of a single module with a limited number of sources (NVIDIA docs, peer-reviewed papers), a manual approach is sufficient and avoids introducing external dependencies. It provides full control over formatting.

**Alternatives considered**:
- **Using a Docusaurus plugin (e.g., `docusaurus-plugin-bibtex`)**: Rejected because it adds complexity and a build-time dependency. While powerful, it's overkill for the current requirements.
- **Embedding a third-party service**: Rejected due to reliance on external services and potential for broken links or service-level changes.
