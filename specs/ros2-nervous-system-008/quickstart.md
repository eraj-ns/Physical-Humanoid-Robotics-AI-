---
id: specs-008-ros2-nervous-system-quickstart
---
# Quickstart: Module 1: The Robotic Nervous System (ROS 2) Contribution Workflow

This guide provides a quickstart for contributing to "Module 1: The Robotic Nervous System (ROS 2)".

## 1. Local Development Environment

1.  **Prerequisites**: Ensure you have Node.js (v20.0 or higher) and npm installed for Docusaurus development. ROS 2 Humble or newer should be installed on an Ubuntu 22.04 LTS system.
2.  **Clone the repository**: `git clone <repository-url>`
3.  **Navigate to the Book directory**: `cd Book_Write/Book`
4.  **Install Docusaurus dependencies**: `npm install`

## 2. Writing and Editing Content

1.  **Locate the files**: The Markdown files for Module 1 will be located in `Book/docs/Module1/`.
2.  **Create new chapters**: Create new `.md` files in the appropriate directory.
3.  **Follow the structure**: Adhere to the Markdown structure defined in `specs/008-ros2-nervous-system/research.md`.
4.  **Start the Docusaurus development server**: Run `npm start` in the `Book/` directory to see a live preview of your changes at `http://localhost:3000`.

## 3. Building and Testing

1.  **Run the Docusaurus build command**: Before committing your changes, run `npm run build` in the `Book/` directory.
2.  **Verify the Docusaurus build**: This command will build the static site into the `Book/build` directory. Ensure that the build process completes without errors.
3.  **Validate ROS 2 Code Examples**: Manually test any ROS 2 Python (`rclpy`) or URDF examples provided in the chapters within a ROS 2 Humble+ environment (e.g., Gazebo simulation).

## 4. Publishing

1.  **Commit and push**: Commit your changes to the feature branch and push to the remote repository.
2.  **Create a Pull Request**: Create a pull request to merge the feature branch into `main`.
3.  **Automated Deployment**: Upon merging, a GitHub Actions workflow will automatically deploy the changes to GitHub Pages.

## 5. Quality Validation Checklist

- [ ] All content is technically accurate for ROS 2 Humble+ and `rclpy`.
- [ ] All code examples are runnable and tested in a ROS 2 Humble+ environment.
- [ ] The Docusaurus site builds successfully without any errors.
- [ ] The formatting is clean, readable, and consistent with the rest of the book.
- [ ] All chapters are complete and meet the requirements of the spec (2500-3500 words).
- [ ] The module clearly explains ROS 2 architecture, communication patterns, `rclpy` control, and URDF modeling.
