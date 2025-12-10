// @ts-check
const { themes: prismThemes } = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical Humanoid Robotics & AI',
  tagline: 'Open Research-Based Engineering Book',
  favicon: 'img/favicon.ico',

  url: 'https://physical-humanoid-robotics-ai.vercel.app',
  baseUrl: '/',

  organizationName: 'eraj-ns',
  projectName: 'Physical-Humanoid-Robotics-AI',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: 'docs',
          routeBasePath: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/eraj-ns/Physical-Humanoid-Robotics-AI/edit/main/',
        },

        blog: false,

        theme: {},
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Humanoid AI Book',
      logo: {
        alt: 'Humanoid Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          href: 'https://github.com/eraj-ns/Physical-Humanoid-Robotics-AI',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Book',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/eraj-ns/Physical-Humanoid-Robotics-AI',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Eraj Naz.`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

module.exports = config;
