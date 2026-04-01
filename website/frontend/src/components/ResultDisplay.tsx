
const ResultDisplay = ({ data, onReset }: any) => {
  if (!data) return null;

  const themeColor = data.isHit ? '#1db954' : '#ff4444';
  const themeGradient = data.isHit 
    ? 'linear-gradient(135deg, #1db954, #1ed760)' 
    : 'linear-gradient(135deg, #ff4444, #ff6b6b)';

  return (
    <div className="analysis-card" style={{ maxWidth: '900px', margin: '0 auto', animation: 'fadeIn 0.8s ease-out', '--theme-color': themeColor } as React.CSSProperties}>
      <div className="glass-panel" style={{ padding: '3rem', borderTop: `4px solid ${themeColor}` }}>
        {/* Track Title Section */}
        <div style={{ marginBottom: '3rem', textAlign: 'center' }}>
          <div style={{ color: themeColor, fontSize: '0.8rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '3px', marginBottom: '0.5rem' }}>DETAILED AUDIT FOR:</div>
          <h2 style={{ fontSize: '3rem', fontWeight: 900, color: 'white', textTransform: 'uppercase', letterSpacing: '-1.5px', lineHeight: 1.1 }}>
             "{data.trackName || 'UNTITLED TRACK'}"
          </h2>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(320px, 1fr) 1.5fr', gap: '3rem' }}>
          
          {/* Result Summary Column */}
          <div style={{ textAlign: 'center', borderRight: '1px solid rgba(255,255,255,0.1)', paddingRight: '2rem' }}>
            <div 
              className="score-badge" 
              style={{ 
                background: themeGradient, 
                color: data.isHit ? 'black' : 'white',
                fontSize: '1.2rem',
                fontWeight: 900,
                padding: '1rem 2.5rem',
                borderRadius: '50px',
                display: 'inline-block',
                boxShadow: `0 10px 30px ${data.isHit ? 'rgba(29, 185, 84, 0.4)' : 'rgba(255, 68, 68, 0.4)'}`,
                textTransform: 'uppercase'
              }}
            >
              {data.isHit ? '🚀 ELITE HIT POTENTIAL' : '⛔ PROBABLE FLOP'}
            </div>
            
            <div style={{ marginTop: '2.5rem' }}>
              <div style={{ fontSize: '5rem', fontWeight: 900, color: 'white', lineHeight: 1, letterSpacing: '-2px' }}>{data.probability}%</div>
              <div style={{ fontSize: '0.9rem', color: '#b3b3b3', marginTop: '0.5rem', textTransform: 'uppercase', letterSpacing: '2px' }}>Voter Confidence</div>
            </div>

            <div style={{ marginTop: '2.5rem', padding: '1.5rem', background: 'rgba(255,255,255,0.03)', borderRadius: '15px', textAlign: 'left', borderLeft: `4px solid ${themeColor}` }}>
              <div style={{ color: themeColor, fontSize: '0.85rem', fontWeight: 800, marginBottom: '0.8rem', letterSpacing: '1px' }}>🧠 AI ANALYSIS REPORT</div>
              <p style={{ fontSize: '1rem', color: '#e0e0e0', lineHeight: '1.7', fontStyle: 'italic', fontWeight: 400 }}>
                "{data.reasoning || 'Our models have flagged this track as having properties that significantly deviate from current hit trends.'}"
              </p>
            </div>
          </div>

          {/* Deep-Dive Grid Column */}
          <div style={{ textAlign: 'left' }}>
            <h4 style={{ color: 'white', marginBottom: '1.5rem', fontSize: '1rem', letterSpacing: '2px', fontWeight: 800 }}>PARAMETER BREAKDOWN</h4>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.2rem' }}>
              {data.analysis.map((item: any, idx: number) => (
                <div key={idx} className="feature-item-glow" style={{ 
                  background: 'rgba(255,255,255,0.03)', 
                  padding: '1.3rem', 
                  borderRadius: '14px', 
                  border: '1px solid rgba(255,255,255,0.08)',
                  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                }}>
                  <div style={{ color: '#888', fontSize: '0.7rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: '0.4rem', letterSpacing: '1px' }}>{item.feature}</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 900, color: 'white' }}>{item.value}</div>
                  <div style={{ fontSize: '0.75rem', color: themeColor, marginTop: '0.3rem', fontWeight: 600 }}>{item.impact}</div>
                </div>
              ))}
            </div>

            <button className="btn-secondary" style={{ marginTop: '2.5rem', width: '100%', border: `1px dashed ${themeColor}`, color: 'white' }} onClick={onReset}>
              ANALYZE ANOTHER TRACK
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;
