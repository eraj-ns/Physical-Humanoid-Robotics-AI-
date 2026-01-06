// For Docusaurus, we need to pass environment variables differently
// This file will be used to set environment variables at build time
const path = require('path');

module.exports = {
  // This is needed for environment variables to be available in the browser
  plugins: [
    [
      require.resolve('@docusaurus/plugin-client-redirects'),
      {
        createRedirects(existingPath) {
          // No redirects needed for this project
        },
      },
    ],
  ],
  themeConfig: {
    // Other theme config...
  },
  // Make sure environment variables are available in the client
  clientModules: [
    path.resolve(__dirname, './src/client/env.js'), // If we need to set env vars in client
  ],
};