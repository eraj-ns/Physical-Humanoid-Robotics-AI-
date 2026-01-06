import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Module 1: The Robotic Nervous System (ROS 2)',
    description: (
      <>
        Learn ROS 2 fundamentals, robot control with Python, and URDF for humanoid modeling.
        This module introduces ROS 2 as the central nervous system of humanoid robots.
      </>
    ),
  },
  {
    title: 'Module 2: The Digital Twin (Gazebo & Unity)',
    description: (
      <>
        Explore physics simulation and environment building. Create realistic digital twins
        using Gazebo and Unity with accurate physics, gravity, collisions, and sensor simulation.
      </>
    ),
  },
  {
    title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
    description: (
      <>
        Advanced perception and navigation with NVIDIA Isaac technologies. Learn about
        photorealistic simulation, hardware-accelerated VSLAM, and Nav2 path planning.
      </>
    ),
  },
  {
    title: 'Module 4: Vision-Language-Action (VLA)',
    description: (
      <>
        Connect LLMs with robotic actions. Learn voice-to-action systems, cognitive planning,
        and build an autonomous humanoid capstone project.
      </>
    ),
  },
];

function Feature({ title, description }) {
  // Extract module number from title to create the link
  const moduleNumber = title.match(/Module (\d+)/);
  const moduleLink = moduleNumber ? `/docs/Module${moduleNumber[1]}/intro` : '#';

  return (
    <div className={clsx('col col--3')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
        <div className="margin-vert--md">
          <a
            className="button button--primary button--md"
            href={moduleLink}
          >
            Open Module
          </a>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}