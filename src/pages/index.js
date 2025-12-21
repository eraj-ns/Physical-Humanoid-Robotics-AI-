import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <header className={clsx(styles.bookHero)}>
      <div className="container">
        <div className={styles.bookGrid}>

          <div className={styles.bookContent}>
            <Heading as="h1" className={styles.bookTitle}>
              {siteConfig.title}
            </Heading>

            <p className={styles.bookSubtitle}>{siteConfig.tagline}</p>

            <p className={styles.bookDescription}>
              <b>A complete research-backed textbook on Physical AI & Humanoid Robotics By Eraj Naz.</b>
            </p>

            <div
              className={styles.bookButtons}
              style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}
            >
              {/* ✅ OPEN ALL MODULES (Module1 + Module2 + Module3 + Module4) */}
              
             <Link
              className="button button--primary button--xl"
              to="/docs/Module1/intro"
              style={{ fontSize: '1.8rem', padding: '1.2rem 3rem' }}
             >
             📘 Start Reading
             </Link>

            </div>
          </div>

          <div className={styles.bookImageWrapper}>
            <img
              src="/img/pngwing.com (5).png"
              alt="Book Cover"
              className={styles.bookImage}
            />
          </div>

        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout title={siteConfig.title} description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
