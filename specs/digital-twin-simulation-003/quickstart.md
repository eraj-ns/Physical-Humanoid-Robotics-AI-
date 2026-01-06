---
id: specs-003-digital-twin-simulation-quickstart
---
# Quickstart: Building and Previewing the Textbook

This guide provides instructions on how to set up the Docusaurus project, build it, and preview the textbook locally.

## 1. Prerequisites

- [Node.js](https://nodejs.org/en/) (version 16.14 or later)
- [Yarn](https://yarnpkg.com/) (optional, but recommended)

## 2. Project Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or
    yarn install
    ```

## 3. Local Development

To start a local development server and preview the textbook in your browser:

```bash
npm run start
# or
yarn start
```

This command will start a local development server and open up a browser window. Most changes are reflected live without having to restart the server. The default URL is `http://localhost:3000`.

## 4. Building the Site

To generate a static build of the textbook:

```bash
npm run build
# or
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## 5. Serving the Build Locally

To preview the production build locally:

```bash
npm run serve
# or
yarn serve
```

This command will serve the content of the `build` directory locally. The default URL is `http://localhost:3000`.

## 6. Project Structure Overview

- `/docs`: Contains the Markdown files for the textbook chapters.
- `/src`: Contains custom React components and styling.
- `/static`: Contains static assets like images.
- `docusaurus.config.js`: The main configuration file for the Docusaurus site.
- `sidebars.js`: Defines the navigation structure of the textbook.
