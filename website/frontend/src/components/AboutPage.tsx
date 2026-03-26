
import { useState } from 'react';

const AboutPage = ({ isFirstTime }: any) => {
  const [shouldAnimate] = useState(isFirstTime);

  return (
    <section className="hero" style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div className="container" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
        <div className={`hero-header ${shouldAnimate ? 'animate-in' : ''}`}>
          <h1>About <span>Project</span></h1>
          <p>Why this project is needed in the modern streaming era.</p>
        </div>

        <div className="hero-body">
          <div className={`hero-text-side glass-panel ${shouldAnimate ? 'animate-in' : ''}`} style={{ padding: '2rem' }}>
            <h3 style={{ color: 'var(--brand-green)', marginBottom: '1.5rem', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '2px' }}>
              The Challenge
            </h3>
            <p style={{ fontSize: '1rem', lineHeight: '1.8', color: 'var(--text-main)' }}>
              With over 100,000 new tracks uploaded to streaming platforms daily, artists and labels face immense pressure to understand listener preferences. Conventional intuition is no longer enough to navigate the algorithmic landscape of modern music discovery.
            </p>
          </div>
          <div className={`hero-form-side glass-panel ${shouldAnimate ? 'animate-in' : ''}`} style={{ padding: '2rem' }}>
            <h3 style={{ color: 'var(--brand-green)', marginBottom: '1.5rem', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '2px' }}>
              Our Goal
            </h3>
            <p style={{ fontSize: '1rem', lineHeight: '1.8', color: 'var(--text-main)' }}>
              We leverage machine learning to quantify the "vibe" of a track. By analyzing 13 acoustic dimensions—from danceability to instrumentalness—we provide empirical evidence of a song's chart-topping potential.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutPage;
