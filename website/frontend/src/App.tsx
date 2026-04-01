import { useState, useEffect } from 'react';
import Navbar from './components/Navbar.tsx';
import Hero from './components/Hero.tsx';
import ModelsPage from './components/ModelsPage.tsx';
import AboutPage from './components/AboutPage.tsx';
import Footer from './components/Footer.tsx';

const App = () => {
  const [activePage, setActivePage] = useState('home');
  const [prediction, setPrediction] = useState<any>(null);
  const [sortKey, setSortKey] = useState('accuracy');
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [visitedPages, setVisitedPages] = useState<Record<string, boolean>>({});

  useEffect(() => {
    // Initial page load delay to trigger first animation
    const timer = setTimeout(() => {
      setVisitedPages(prev => ({ ...prev, [activePage]: true }));
    }, 1000);

    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20,
      });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      clearTimeout(timer);
    };
  }, []);

  const handlePageChange = (page: string) => {
    setActivePage(page);
    if (!visitedPages[page]) {
      setTimeout(() => {
        setVisitedPages(prev => ({ ...prev, [page]: true }));
      }, 500);
    }
  };

  const tickerItems = [
    'HIT OR FLOP? PREDICTION ENGINE',
    '84.5% MULTI-VOTE ACCURACY',
    'MUSIC SUCCESS BENCHMARKING',
    'REAL-TIME AUDIO ANALYSIS',
    'SHAP EXPLAINABILITY ACTIVE',
    'TRADITIONAL ML BENCHMARKS'
  ];

  return (
    <div className="App" style={{ perspective: '1000px' }}>
      <div className="bg-container" style={{
        transform: `translate3d(${mousePos.x * -1.5}px, ${mousePos.y * -1.5}px, 0)`
      }}>
        <video 
          className="bg-video" 
          autoPlay 
          muted 
          loop 
          poster="https://images.unsplash.com/photo-1493225255756-d9584f8606e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80"
        >
          <source src="https://assets.mixkit.co/videos/preview/mixkit-spinning-vinyl-record-on-a-player-35105-large.mp4" type="video/mp4" />
        </video>
        <div className="bg-overlay"></div>
        <div className="ambient-glow" style={{ 
          top: '20%', left: '10%',
          transform: `translate3d(${mousePos.x * 2}px, ${mousePos.y * 2}px, 0)`
        }}></div>
        <div className="ambient-glow" style={{ 
          bottom: '20%', right: '10%',
          transform: `translate3d(${mousePos.x * -2}px, ${mousePos.y * -2}px, 0)`
        }}></div>
      </div>

      <Navbar activePage={activePage} setActivePage={handlePageChange} />
      
      <div className="content-scroll">
        <div className="sticky-viewport-manager">
          <main className="parallax-layer" style={{
            transform: `translate3d(${mousePos.x * 0.5}px, ${mousePos.y * 0.5}px, 0)`
          }}>
            <div className="page-content-wrapper">
              {activePage === 'home' && (
                <Hero 
                  prediction={prediction} 
                  setPrediction={setPrediction} 
                  isFirstTime={!visitedPages['home']}
                />
              )}
              {activePage === 'models' && (
                <ModelsPage 
                  sortKey={sortKey} 
                  setSortKey={setSortKey} 
                  isFirstTime={!visitedPages['models']}
                />
              )}
              {activePage === 'about' && <AboutPage isFirstTime={!visitedPages['about']} />}
            </div>
          </main>

          <footer className="ticker-footer">
            <div className="ticker-track">
              <div className="ticker-content">
                {tickerItems.map((item, i) => (
                  <div key={i} className="ticker-item">{item}</div>
                ))}
              </div>
              <div className="ticker-content">
                {tickerItems.map((item, i) => (
                  <div key={`dup-${i}`} className="ticker-item">{item}</div>
                ))}
              </div>
            </div>
          </footer>
        </div>

        <Footer />
      </div>
    </div>
  );
};

export default App;
