import { useState } from 'react';

const AboutPage = ({ isFirstTime }: any) => {
  const [shouldAnimate] = useState(isFirstTime);

  const parameters = [
    'ENERGY', 'DANCEABILITY', 'VALENCE', 'ACOUSTICNESS', 
    'INSTRUMENTALNESS', 'LIVENESS', 'SPEECHINESS', 'TEMPO'
  ];

  return (
    <section className="hero" style={{ height: '100vh', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div className="container" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
        
        {/* Header Section */}
        <div className={`hero-header ${shouldAnimate ? 'animate-in' : ''}`} style={{ marginBottom: '3rem', textAlign: 'center' }}>
          <h1 style={{ fontSize: '3.5rem' }}>The <span>Technology</span> Behind Hits</h1>
          <p style={{ maxWidth: '800px', margin: '0.5rem auto' }}>
            Bridging the gap between subjective art and objective data science. 
            We turn musical vibrations into actionable predictions.
          </p>
        </div>

        {/* 3-Column Grid */}
        <div className="hero-body" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '3rem' }}>
          
          <div className={`glass-panel ${shouldAnimate ? 'animate-in' : ''}`} style={{ padding: '2.5rem', transitionDelay: '0.1s' }}>
            <h3 style={{ color: 'var(--theme-color)', marginBottom: '1.5rem', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '2.5px' }}>
              The Challenge
            </h3>
            <p style={{ fontSize: '0.95rem', lineHeight: '1.8', color: 'var(--text-main)' }}>
              In a world where 100k+ songs are uploaded daily, intuition fails. 
              Artists need more than just hope, they need empirical data to cut through the noise of the global streaming landscape.
            </p>
          </div>

          <div className={`glass-panel ${shouldAnimate ? 'animate-in' : ''}`} style={{ padding: '2.5rem', border: '1px solid var(--theme-color)', transitionDelay: '0.2s' }}>
            <h3 style={{ color: 'var(--theme-color)', marginBottom: '1.5rem', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '2.5px' }}>
              Our Methodology
            </h3>
            <p style={{ fontSize: '0.95rem', lineHeight: '1.8', color: 'var(--text-main)' }}>
              We extract 13 core acoustic dimensions directly from the raw audio waveform. 
              Our Multi Vote Ensemble model benchmarks these patterns against a decade of chart historical success.
            </p>
          </div>

          <div className={`glass-panel ${shouldAnimate ? 'animate-in' : ''}`} style={{ padding: '2.5rem', transitionDelay: '0.3s' }}>
            <h3 style={{ color: 'var(--theme-color)', marginBottom: '1.5rem', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '2.5px' }}>
              The Future
            </h3>
            <p style={{ fontSize: '0.95rem', lineHeight: '1.8', color: 'var(--text-main)' }}>
              Our platform aims to democratize the music labels' secret sauce, providing 
              high accuracy analytical insights previously only accessible to major industry 
              conglomerates and data heavy record labels.
            </p>
          </div>
        </div>

        {/* Technical Perimeter Section */}
        <div className={`animate-in`} style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0.8rem', transitionDelay: '0.5s' }}>
          {parameters.map((param) => (
            <span key={param} style={{
              padding: '6px 14px',
              borderRadius: '20px',
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(255,255,255,0.06)',
              color: 'var(--text-dim)',
              fontSize: '0.65rem',
              letterSpacing: '1px',
              fontWeight: 600,
              textTransform: 'uppercase'
            }}>
              {param}
            </span>
          ))}
        </div>

        {/* Branding Footer removed due to redundancy with global footer */}

      </div>
    </section>
  );
};

export default AboutPage;
