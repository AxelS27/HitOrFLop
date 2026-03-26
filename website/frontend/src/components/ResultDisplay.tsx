
const ResultDisplay = ({ data, onReset }: any) => {
  if (!data) return null;

  return (
    <div className="analysis-card">
      <div className="glass-panel" style={{ textAlign: 'center' }}>
        <div style={{ marginBottom: '2rem' }}>
          <div 
            className="score-badge" 
            style={{ 
              background: data.isHit ? '#1db954' : '#ff4444', 
              color: data.isHit ? 'black' : 'white',
              fontSize: '1.2rem',
              padding: '1rem 3rem'
            }}
          >
            {data.isHit ? 'A POTENTIAL HIT!' : 'LIKELY A FLOP...'}
          </div>
          <p style={{ color: 'white', fontSize: '2rem', fontWeight: 900, marginTop: '1rem' }}>
            {data.probability}% <span style={{ fontSize: '1rem', fontWeight: 400, color: '#b3b3b3' }}>Hit Probability</span>
          </p>
          <p style={{ fontSize: '0.8rem', color: '#b3b3b3', marginTop: '0.5rem' }}>Calculated using <strong>{data.model}</strong></p>
        </div>

        <div style={{ textAlign: 'left', marginTop: '3rem' }}>
          <h4 style={{ color: 'white', marginBottom: '1.5rem', fontSize: '1.1rem', letterSpacing: '1px' }}>MODEL ANALYTICAL DEEP-DIVE</h4>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1.5rem' }}>
            {data.analysis.map((item: any, idx: number) => (
              <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)' }}>
                <div style={{ color: '#1db954', fontSize: '0.7rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: '0.5rem' }}>{item.feature}</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem' }}>{item.value}</div>
                <div style={{ fontSize: '0.75rem', color: '#b3b3b3' }}>{item.impact}</div>
              </div>
            ))}
          </div>
        </div>

        <button className="btn-secondary" style={{ marginTop: '3rem' }} onClick={onReset}>
          ANALYZE ANOTHER TRACK
        </button>
      </div>
    </div>
  );
};

export default ResultDisplay;
