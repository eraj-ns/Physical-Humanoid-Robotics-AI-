import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Module 1 — The Robotic Nervous System (ROS 2)',
    link: '/docs/module1',
    description:
      'ROS 2 middleware, nodes, topics, services, Python agents, and humanoid URDF modeling.',
  },
  {
    title: 'Module 2 — The Digital Twin (Gazebo & Unity)',
    link: '/docs/module2',
    description:
      'Physics simulation, realistic environments, sensor modeling, and virtual testing.',
  },
  {
    title: 'Module 3 — The AI-Robot Brain (NVIDIA Isaac™)',
    link: '/docs/module3',
    description:
      'Photorealistic simulation, Isaac ROS, VSLAM, and humanoid navigation with Nav2.',
  },
  {
    title: 'Module 4 — Vision-Language-Action (VLA)',
    link: '/docs/module4',
    description:
      'LLMs for robotics, voice commands, cognitive planning, and autonomous humanoid capstone.',
  },
];

function Feature({ title, description, link }) {
  return (
    <div className={clsx('col col--3', styles.featureCard)}>
      <div className="padding--lg">
        <Heading as="h3" className={styles.featureTitle}>
          {title}
        </Heading>

        <p className={styles.featureText}>{description}</p>

        <Link className="button button--sm button--primary" to={link}>
          Open Module →
        </Link>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <Heading as="h2" className="text--center margin-bottom--lg">
          Book Modules
        </Heading>

        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
