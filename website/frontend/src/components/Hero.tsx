import { useState } from 'react';
import PredictorForm from './PredictorForm.tsx';
import ResultDisplay from './ResultDisplay.tsx';

const Hero = ({ prediction, setPrediction, isFirstTime }: any) => {
  const [loading, setLoading] = useState(false);
  const [shouldAnimate] = useState(isFirstTime);

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
                  Harness the power of Multi-Vote Ensemble and Big 5 Models to decode the DNA of a music hit. 
                  Upload your demo or link any track to see if it's destined for the charts.
                </p>
              </div>
              <div className={`hero-form-side ${shouldAnimate ? 'animate-in' : ''}`}>
                <PredictorForm onStart={() => setLoading(true)} onResult={(res: any) => {
                  setPrediction(res);
                  setLoading(false);
                }} />
              </div>
            </div>
          </>
        ) : loading ? (
          <div className="loading-state">
             <div className="score-badge">Analyzing Audio Characteristics...</div>
             <p>Our model is processing 60 parameters per second...</p>
          </div>
        ) : (
          <ResultDisplay data={prediction} onReset={() => setPrediction(null)} />
        )}
      </div>
    </section>
  );
};

export default Hero;
