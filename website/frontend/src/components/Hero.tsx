import { useState } from 'react';
import PredictorForm from './PredictorForm.tsx';
import ResultDisplay from './ResultDisplay.tsx';

const Hero = ({ prediction, setPrediction, loading, setLoading, progress, factIndex, facts, isFirstTime, onDnaClick }: any) => {
  const [shouldAnimate] = useState(isFirstTime);

  // Handle the completion of loading to create a smooth 100% fill before switching
  const handleResult = (res: any) => {
    setPrediction(res);
  };

  return (
    <section className="hero">
      <div className="container" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        {!prediction && !loading ? (
          <>
            <div className={`hero-header ${shouldAnimate ? 'animate-in' : ''}`} style={{ marginBottom: '2rem' }}>
              <h1>Music Hit <span>Predictor</span></h1>
              <h2>ML Powered Analysis</h2>
            </div>
            <div className="hero-body">
              <div className={`hero-text-side ${shouldAnimate ? 'animate-in' : ''}`}>
                <p>
                  Harness our Multi Vote Ensemble intelligence to decode the acoustic DNA of potential hits. 
                  Optimized against 52,616 balanced tracks across 125 unique genres to provide high-precision predictive analytics.
                </p>
              </div>
              <div className={`hero-form-side ${shouldAnimate ? 'animate-in' : ''}`}>
                <PredictorForm onStart={() => setLoading(true)} onResult={handleResult} />
              </div>
            </div>
          </>
        ) : loading ? (
          <div className="loading-state" style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto', width: '100%', animation: 'none' }}>
             <div className="score-badge">Decoding Audio DNA...</div>
             
             <div style={{ 
               width: '100%', height: '4px', background: 'rgba(255,255,255,0.05)', 
               borderRadius: '10px', marginTop: '2.5rem', marginBottom: '1.5rem',
               overflow: 'hidden', position: 'relative'
             }}>
               <div style={{ 
                 width: `${progress}%`, height: '100%', 
                 background: 'var(--theme-color)', transition: 'width 0.1s linear', 
                 boxShadow: '0 0 10px var(--theme-color-faded)'
               }} />
             </div>
             
             <p style={{ color: 'var(--text-dim)', fontSize: '0.9rem', fontStyle: 'italic', letterSpacing: '0.5px' }}>
                {facts[factIndex]}
             </p>
          </div>
        ) : (
          <ResultDisplay data={prediction} onReset={() => setPrediction(null)} onDnaClick={onDnaClick} />
        )}
      </div>
    </section>
  );
};

export default Hero;
