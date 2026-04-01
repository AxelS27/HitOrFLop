import { useState, useEffect } from 'react';
import Navbar from './components/Navbar.tsx';
import Hero from './components/Hero.tsx';
import ModelsPage from './components/ModelsPage.tsx';
import AboutPage from './components/AboutPage.tsx';
import DNAVisualizer from './components/DNAVisualizer.tsx';
import Footer from './components/Footer.tsx';
import bgVideo from './assets/background_video.mp4';

const App = () => {
  /* --- GLOBAL STATE MANAGEMENT --- */
  const [activePage, setActivePage] = useState('home');
  const [prediction, setPrediction] = useState<any>(() => {
    const saved = localStorage.getItem('last_prediction');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [factIndex, setFactIndex] = useState(0);
  const [sortKey, setSortKey] = useState('accuracy');
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [visitedPages, setVisitedPages] = useState<Record<string, boolean>>({});
  const [isDnaOpen, setIsDnaOpen] = useState(false);

  /* --- TECHNICAL PROTOCOLS (LOADING FACTS) --- */
  const facts = [
    "Analyzing 13 acoustic dimensions including spectral energy...",
    "Processing audio samples at 22,050Hz for peak precision...",
    "Benchmarking results across 6 distinct ML algorithms...",
    "Performing Multi-Vote Ensemble check for final consensus...",
    "Comparing frequency patterns with 52,616 balanced samples...",
    "Validating SHAP values for explainable AI reasoning..."
  ];

  /* --- CORE EFFECT HOOKS --- */
  useEffect(() => {
    let interval: any;
    let progressInterval: any;

    if (loading) {
      interval = setInterval(() => {
        setFactIndex((prev) => (prev + 1) % facts.length);
      }, 2500);

      progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 92) return prev;
          return prev + 0.15; 
        });
      }, 50);
    }

    return () => {
      clearInterval(interval);
      clearInterval(progressInterval);
    };
  }, [loading]);

  useEffect(() => {
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
  }, [activePage]);

  /* --- EVENT HANDLERS --- */
  const handlePageChange = (page: string) => {
    setActivePage(page);
    if (!visitedPages[page]) {
      setTimeout(() => {
        setVisitedPages(prev => ({ ...prev, [page]: true }));
      }, 500);
    }
  };

  const updatePrediction = (res: any) => {
    if (res) {
      setProgress(100);
      setTimeout(() => {
        setPrediction(res);
        setLoading(false);
        localStorage.setItem('last_prediction', JSON.stringify(res));
      }, 600);
    } else {
      setPrediction(null);
      setProgress(0);
      setFactIndex(0);
      localStorage.removeItem('last_prediction');
    }
  };

  /* --- UI MODULES --- */
  const tickerItems = [
    'HIT OR FLOP? PREDICTION ENGINE',
    '84.5% MULTI VOTE ACCURACY',
    'MUSIC SUCCESS BENCHMARKING',
    'REAL TIME AUDIO ANALYSIS',
    'SHAP EXPLAINABILITY ACTIVE',
    'TRADITIONAL ML BENCHMARKS',
    'GROUP 3 PROJECT'
  ];

  const themeColor = prediction ? (prediction.isHit ? '#1db954' : '#ff4444') : '#1db954';
  const themeColorFaded = prediction ? (prediction.isHit ? 'rgba(29, 185, 84, 0.15)' : 'rgba(255, 68, 68, 0.25)') : 'rgba(29, 185, 84, 0.15)';

  /* --- RENDER LOGIC --- */
  return (
    <div className="App" style={{ 
      perspective: '1000px',
      '--theme-color': themeColor,
      '--theme-color-faded': themeColorFaded
    } as React.CSSProperties}>
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
          <source src={bgVideo} type="video/mp4" />
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
                  setPrediction={updatePrediction} 
                  loading={loading}
                  setLoading={setLoading}
                  progress={progress}
                  factIndex={factIndex}
                  facts={facts}
                  isFirstTime={!visitedPages['home']}
                  onDnaClick={() => setIsDnaOpen(true)}
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

      <DNAVisualizer isOpen={isDnaOpen} onClose={() => setIsDnaOpen(false)} prediction={prediction} />
    </div>
  );
};

export default App;
