---
id: specs-003-digital-twin-simulation-research
---
# Research: Docusaurus for Technical Book Writing

This document summarizes the research findings for building a technical textbook using Docusaurus.

## 1. Docusaurus Architecture for Technical Books

**Decision**: Docusaurus is a suitable platform for this project.

**Rationale**:

*   **Static Site Generation**: Docusaurus builds a static site from Markdown files, which is fast, secure, and easy to deploy.
*   **Content-focused**: It uses MDX (Markdown with JSX), allowing for rich content with embedded React components. This is ideal for interactive examples.
*   **Structured Content**: The `docs` directory and `sidebars.js` file provide a clear structure for organizing the book into modules and chapters.
*   **"Docs as Code"**: The entire project can be managed in a Git repository, enabling version control, collaboration, and automated builds.
*   **Extensibility**: Docusaurus has a pluggable architecture and can be customized with React components.

**Alternatives Considered**:

*   **GitBook**: A commercial platform for technical documentation. Docusaurus was chosen for its open-source nature and greater customization options.
*   **Jekyll**: Another popular static site generator. Docusaurus was preferred for its modern toolchain (React, MDX) and features tailored for documentation.

## 2. Markdown and APA Citations

**Decision**: We will use manual APA citation formatting within Markdown files.

**Rationale**:

*   Docusaurus does not have a built-in APA citation manager.
*   Manual formatting provides full control over the presentation of citations.
*   For in-text citations, we will use the `(Author, Year)` format.
*   A dedicated "References" section will be included at the end of each chapter or module, listing all sources in APA 7th edition style.

**Alternatives Considered**:

*   **Custom React Components**: Creating custom `<Cite>` and `<ReferenceList>` components was considered. This was rejected for the initial phase to reduce complexity, but may be revisited later.
*   **Remark/Rehype Plugins**: Exploring third-party plugins for citation management. No mature and widely adopted plugin for APA citations was found.

## 3. Build and Deployment to GitHub Pages

**Decision**: We will use a GitHub Actions workflow for automated builds and deployments.

**Rationale**:

*   **Automation**: A CI/CD pipeline with GitHub Actions will automatically build and deploy the site whenever changes are pushed to the `main` branch.
*   **Reliability**: This approach ensures that the deployed site is always up-to-date and reduces the risk of manual deployment errors.
*   **Configuration**: The `docusaurus.config.js` file will be configured with the appropriate `url`, `baseUrl`, `organizationName`, and `projectName` for GitHub Pages.

**Alternatives Considered**:

*   **Manual Deployment with `gh-pages`**: This approach is simpler to set up but is more error-prone and less scalable than using GitHub Actions.

## 4. RAG (Retrieval-Augmented Generation) Integration

**Decision**: RAG integration is a potential future enhancement, but will not be part of the initial implementation.

**Rationale**:

*   **Complexity**: Integrating a RAG system adds significant complexity, requiring a separate backend service, vector database, and LLM orchestration.
*   **Cost**: LLM and vector database usage can be expensive.
*   **Focus on Core Content**: The primary goal is to create high-quality textbook content. RAG integration is a "bonus feature" that can be added later.

**Architectural Sketch (for future reference)**:

*   **Backend**: A Python-based backend using FastAPI.
*   **Orchestration**: LangChain or LlamaIndex.
*   **Vector Database**: ChromaDB for local development, Pinecone or Weaviate for production.
*   **Frontend**: Custom React components within Docusaurus to query the RAG backend.
*   **APIs**: Endpoints for `/query` and `/ingest`.

By deferring RAG integration, we can focus on delivering the core textbook content first, while keeping the door open for this advanced feature in the future.
