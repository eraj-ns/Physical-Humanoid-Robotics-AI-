---
id: specs-007-vla-module-quickstart
---
# Quickstart: VLA Module Contribution Workflow

This guide provides a quickstart for contributing to the Vision-Language-Action (VLA) module.

## 1. Local Development Environment

1.  **Prerequisites**: Ensure you have Node.js (v20.0 or higher) and npm installed.
2.  **Clone the repository**: `git clone <repository-url>`
3.  **Navigate to the Book directory**: `cd Book_Write/Book`
4.  **Install dependencies**: `npm install`

## 2. Writing and Editing Content

1.  **Locate the files**: The Markdown files for Module 4 are located in `Book/docs/Module4/`.
2.  **Create new chapters**: Create new `.md` files in the appropriate directory.
3.  **Follow the structure**: Adhere to the Markdown structure defined in `specs/007-vla-module/research.md`.
4.  **Start the development server**: Run `npm start` in the `Book/` directory to see a live preview of your changes at `http://localhost:3000`.

## 3. Building and Testing

1.  **Run the build command**: Before committing your changes, run `npm run build` in the `Book/` directory.
2.  **Verify the build**: This command will build the static site into the `Book/build` directory. Ensure that the build process completes without errors.

## 4. Publishing

1.  **Commit and push**: Commit your changes to the feature branch and push to the remote repository.
2.  **Create a Pull Request**: Create a pull request to merge the feature branch into `main`.
3.  **Automated Deployment**: Upon merging, a GitHub Actions workflow will automatically deploy the changes to GitHub Pages.

## 5. QA Checklist

- [ ] All content is technically accurate for ROS 2, Gazebo, and NVIDIA Isaac Sim.
- [ ] All code examples are runnable and tested.
- [ ] The Docusaurus site builds successfully without any errors.
- [ ] The formatting is clean, readable, and consistent with the rest of the book.
- [ ] All chapters are complete and meet the requirements of the spec.
