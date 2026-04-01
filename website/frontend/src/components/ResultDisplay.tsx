
const ResultDisplay = ({ data, onReset, onDnaClick }: any) => {
  if (!data) return null;

  /* --- THEME CONFIGURATION --- */
  const themeColor = data.isHit ? '#1db954' : '#ff4444';
  const themeGradient = data.isHit 
    ? 'linear-gradient(135deg, #1db954, #1ed760)' 
    : 'linear-gradient(135deg, #ff4444, #ff6b6b)';

  return (
    <div className="analysis-card" style={{ maxWidth: '1400px', width: '98%', margin: '0 auto', animation: 'fadeIn 0.8s ease-out', '--theme-color': themeColor } as React.CSSProperties}>
      <div className="glass-panel" style={{ padding: '2rem 3rem', borderTop: `4px solid ${themeColor}` }}>
        
        {/* --- REPORT HEADER SECTION --- */}
        <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
          <div style={{ 
            background: themeColor, 
            color: 'white', 
            fontSize: '0.7rem', 
            fontWeight: 800, 
            textTransform: 'uppercase', 
            letterSpacing: '2px', 
            padding: '0.2rem 0.8rem', 
            borderRadius: '4px', 
            display: 'inline-block',
            marginBottom: '0.4rem' 
          }}>AUDIT REPORT FOR:</div>
          <h2 style={{ fontSize: '2.8rem', fontWeight: 900, color: 'white', textTransform: 'uppercase', letterSpacing: '-1.5px', lineHeight: 1, margin: 0 }}>
             "{data.trackName || 'UNTITLED'}"
          </h2>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.8fr 1fr', gap: '2rem', alignItems: 'start' }}>
          
          {/* --- COLUMN 1: ANALYTIC SUMMARY --- */}
          <div style={{ textAlign: 'center', borderRight: '1px solid rgba(255,255,255,0.08)', paddingRight: '1.5rem' }}>
            <div 
              className="score-badge" 
              style={{ 
                background: themeGradient, 
                color: data.isHit ? 'black' : 'white',
                fontSize: '0.9rem',
                fontWeight: 900,
                padding: '0.6rem 1.8rem',
                borderRadius: '50px',
                display: 'inline-block',
                textTransform: 'uppercase'
              }}
            >
              {data.isHit ? 'ELITE HIT' : 'PROBABLE FLOP'}
            </div>
            
            <div style={{ marginTop: '1.5rem' }}>
              <div style={{ fontSize: '5.5rem', fontWeight: 900, color: 'white', lineHeight: 0.9, letterSpacing: '-3px' }}>{data.probability}%</div>
              <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.3rem', textTransform: 'uppercase', letterSpacing: '2px' }}>Confidence Score</div>
            </div>

            <button 
                onClick={onReset}
                className="btn-secondary"
                style={{ marginTop: '2.5rem', width: '100%', fontSize: '0.7rem', padding: '0.8rem' }}
              >
                ← NEW ANALYSIS
              </button>
          </div>

          {/* --- COLUMN 2: PARAMETRIC DEEP-DIVE --- */}
          <div style={{ borderRight: '1px solid rgba(255,255,255,0.08)', paddingRight: '1.5rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem' }}>
              {data.analysis.map((item: any, idx: number) => (
                <div key={idx} className="feature-item-glow" style={{ position: 'relative', background: 'rgba(255,255,255,0.02)', padding: '1rem 1.2rem', borderRadius: '12px' }}>
                  <div style={{ color: '#777', fontSize: '0.6rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '0.25rem' }}>{item.feature}</div>
                  <div style={{ color: 'white', fontSize: '1.4rem', fontWeight: 900 }}>
                    {typeof item.value === 'string' ? item.value.replace(/[^\x00-\x7F]/g, "") : item.value}
                  </div>
                  <div style={{ color: themeColor, fontSize: '0.7rem', fontWeight: 600, marginTop: '0.2rem' }}>{item.impact}</div>
                </div>
              ))}
            </div>
          </div>

          {/* --- COLUMN 3: AI REASONING & PROTOCOLS --- */}
          <div style={{ textAlign: 'left', display: 'flex', flexDirection: 'column' }}>
            <div style={{ color: themeColor, fontSize: '0.8rem', fontWeight: 800, marginBottom: '0.8rem', letterSpacing: '1px' }}>AI LOGIC REPORT</div>
            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1.5rem', borderRadius: '15px', borderLeft: `4px solid ${themeColor}`, marginBottom: '1.5rem' }}>
              <p style={{ fontSize: '1rem', color: '#bbb', lineHeight: '1.6', fontStyle: 'italic', margin: 0 }}>
                "{data.reasoning || 'Stability analysis suggests standard market alignment.'}"
              </p>
            </div>
            
            <button 
                onClick={onDnaClick}
                style={{ 
                  marginTop: 'auto', width: '100%', fontSize: '0.65rem', padding: '1rem',
                  letterSpacing: '1.5px', background: 'rgba(255,255,255,0.02)', border: `1px solid ${themeColor}44`,
                  color: 'white', borderRadius: '8px', cursor: 'pointer', fontWeight: 700,
                  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)', textTransform: 'uppercase',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px',
                  boxShadow: `0 4px 15px rgba(0,0,0,0.2)`
                }}
                onMouseOver={(e: any) => { 
                  e.currentTarget.style.background = `${themeColor}22`; 
                  e.currentTarget.style.borderColor = themeColor;
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = `0 8px 25px ${themeColor}22`;
                }}
                onMouseOut={(e: any) => { 
                  e.currentTarget.style.background = 'rgba(255,255,255,0.02)'; 
                  e.currentTarget.style.borderColor = `${themeColor}44`;
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = `0 4px 15px rgba(0,0,0,0.2)`;
                }}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke={themeColor} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M2 10v3M6 6v11M10 3v18M14 8v7M18 5v13M22 10v3"/>
                </svg>
                VIEW SPECTRAL DNA
              </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;
