const path = require('path');

module.exports = function (context, options) {
  const { siteConfig } = context;
  const { environment = {} } = options;

  return {
    name: 'docusaurus-plugin-global-chatbot',

    configureWebpack(config, isServer, utils) {
      return {
        resolve: {
          alias: {
            '@site/src/components/EmbeddedChatbot': path.resolve(
              __dirname,
              '../components/EmbeddedChatbot'
            ),
          },
        },
        plugins: [
          ...(config.plugins || []),
          new (require('webpack')).DefinePlugin({
            'process.env': JSON.stringify({
              ...process.env,
              ...environment,
            }),
          }),
        ],
      };
    },

    getThemePath() {
      return path.resolve(__dirname, './theme');
    },
  };
};