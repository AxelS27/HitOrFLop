import { useEffect, useState, useRef } from 'react';

const DNAVisualizer = ({ isOpen, onClose, prediction }: { isOpen: boolean, onClose: () => void, prediction: any }) => {
  const [logs, setLogs] = useState<string[]>([]);
  const logTerminalRef = useRef<HTMLDivElement>(null);

  /* --- DATA MAPPING HELPERS --- */
  const getFeatureValue = (label: string) => {
    if (!prediction || !prediction.features) return '---';
    const f = prediction.features;
    switch (label) {
      case 'Spectral Centroid': return `${Math.round(f.spectral_centroid || 0)} Hz`;
      case 'RMS Energy': return (f.energy || 0).toFixed(3);
      case 'Chroma STFT': return (f.chroma_stft || 0.45).toFixed(2);
      case 'Zero Crossing': return (f.zcr || 0.08).toFixed(3);
      case 'Tempo Est.': return `${Math.round(f.tempo || 0)} BPM`;
      case 'Loudness': return `${f.loudness?.toFixed(1) || -14.0} LUFS`;
      case 'Key': return ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][f.key] || 'C';
      case 'Mode': return f.mode === 1 ? 'Major' : 'Minor';
      case 'Duration': return `${Math.round((f.duration_ms || 0) / 1000)}s`;
      default: return 'MATCH';
    }
  };

  const technicalParams = [
    { label: 'Spectral Centroid', key: 'Spectral Centroid' },
    { label: 'RMS Energy', key: 'RMS Energy' },
    { label: 'Chroma STFT', key: 'Chroma STFT' },
    { label: 'Zero Crossing', key: 'Zero Crossing' },
    { label: 'Tempo Est.', key: 'Tempo Est.' },
    { label: 'Loudness', key: 'Loudness' },
    { label: 'Key', key: 'Key' },
    { label: 'Mode', key: 'Mode' },
    { label: 'Duration', key: 'Duration' }
  ];

  /* --- TERMINAL LOG GENERATION --- */
  const logPossibilities = prediction ? [
    `ANALYZING_FILE: ${prediction.trackName?.substring(0, 20)}...`,
    `EXTRACTING_FEATURES_FROM_BITSTREAM...`,
    `NORMALIZING_LUFS_TO_-14.0...`,
    `MATCHING_DNA_AGAINST_SPOTIFY_110K...`,
    `CONFIDENCE_SCORE: ${prediction.probability}%`,
    `RESULT: ${prediction.isHit ? 'HIT_PREDICTED' : 'FLOP_PREDICTED'}`,
    'MAPPING_SPECTRAL_ENVELOPE...',
    'CALCULATING_SHAP_EXPLAINABILITY...'
  ] : [
    'SYSTEM_IDLE: STANDBY_MODE',
    'WAITING_FOR_AUDIO_STREAM...',
    'SCANNING_EMPTY_BUFFER...',
    'READY_FOR_FINGERPRINT_INGESTION'
  ];

  useEffect(() => {
    if (!isOpen) return;
    const interval = setInterval(() => {
      const newLog = `[${new Date().toLocaleTimeString()}] ${logPossibilities[Math.floor(Math.random() * logPossibilities.length)]}`;
      setLogs(prev => [...prev.slice(-15), newLog]);
    }, 1000);
    return () => clearInterval(interval);
  }, [isOpen, prediction]);

  useEffect(() => {
    if (logTerminalRef.current) {
      logTerminalRef.current.scrollTop = logTerminalRef.current.scrollHeight;
    }
  }, [logs]);

  if (!isOpen) return null;

  /* --- UI RENDER --- */
  return (
    <div className="dna-overlay" style={{ 
      position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh',
      background: 'rgba(0,0,5,0.98)', backdropFilter: 'blur(15px)',
      zIndex: 9999, padding: '40px', display: 'flex', flexDirection: 'column',
      animation: 'fadeIn 0.4s cubic-bezier(0,0.8,0.2,1)',
      fontFamily: '"SF Mono", "Roboto Mono", monospace'
    }}>
      <div style={{ position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)', backgroundSize: '20px 20px', pointerEvents: 'none' }} />

      {/* --- HEADER --- */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '20px', marginBottom: '30px' }}>
        <div>
          <h2 style={{ fontSize: '1rem', letterSpacing: '8px', color: 'var(--theme-color)', margin: 0 }}>
            {prediction ? 'REAL_DATA_ANALYSIS' : 'SYSTEM_IDLE_MODE'}
          </h2>
          <div style={{ fontSize: '0.6rem', opacity: 0.4, marginTop: '5px' }}>
            {prediction ? `SOURCE: ${prediction.trackName}` : 'AWAITING TRACK UPLOAD FOR DEEP SPECTRAL INSPECTION'}
          </div>
        </div>
        <button onClick={onClose} style={{ 
          background: 'none', border: '1px solid rgba(255,255,255,0.2)', color: 'white', 
          padding: '8px 24px', borderRadius: '4px', cursor: 'pointer', fontSize: '0.7rem'
        }}>
          EXIT_X
        </button>
      </div>

      {/* --- CORE DASHBOARD --- */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(250px, 1fr) 2fr minmax(250px, 1fr)', gap: '30px', flex: 1, overflow: 'visible' }}>
        
        {/* --- LEFT: FINGERPRINT --- */}
        <div className="glass-panel" style={{ padding: '20px', background: 'rgba(255,255,255,0.02)', display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <h3 style={{ fontSize: '0.65rem', letterSpacing: '2px', opacity: 0.5, borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '10px' }}>TRACK_FINGERPRINT</h3>
          {technicalParams.map(param => (
            <div key={param.label} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
              <span style={{ opacity: 0.4 }}>{param.label}</span>
              <span style={{ color: prediction ? 'var(--theme-color)' : 'white', fontWeight: 600 }}>{getFeatureValue(param.key)}</span>
            </div>
          ))}
          <div style={{ marginTop: 'auto', padding: '15px', background: prediction ? 'rgba(29,185,84,0.05)' : 'rgba(255,255,255,0.03)', borderRadius: '4px', border: prediction ? '1px solid var(--theme-color)' : '1px solid rgba(255,255,255,0.1)' }}>
            <div style={{ fontSize: '0.6rem', opacity: 0.6, marginBottom: '5px' }}>FINGERPRINT STATUS</div>
            <div style={{ fontSize: '1rem', fontWeight: 900, color: prediction ? 'var(--theme-color)' : 'white' }}>
                {prediction ? 'MATCHED' : 'AWAITING'}
            </div>
          </div>
        </div>

        {/* --- CENTER: SPECTRAL SCANNER --- */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
          <div className="glass-panel" style={{ 
            flex: 2, 
            background: 'rgba(0,0,0,0.4)', 
            position: 'relative', 
            overflow: 'hidden', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            padding: '60px 40px'
          }}>
            <div style={{ 
              display: 'flex', 
              gap: '4px', 
              alignItems: 'flex-end', 
              height: '100%', 
              width: '100%',
              maxWidth: '1200px'
            }}>
                {[...Array(120)].map((_, i) => (
                    <div key={i} style={{ 
                        flex: 1,
                        height: `${Math.random() * 80 + 20}%`,
                        background: 'var(--theme-color)',
                        opacity: prediction ? (Math.random() * 0.7 + 0.3) : 0.1,
                        borderRadius: '2px 2px 0 0',
                        animation: prediction ? `waveHeight ${0.1 + Math.random()}s linear infinite alternate` : 'none'
                    }} />
                ))}
            </div>
            <div style={{ position: 'absolute', top: '10px', left: '10px', fontSize: '0.6rem', opacity: 0.4 }}>WAVE_SCANNER_ACTIVE</div>
            <div style={{ position: 'absolute', top: 0, left: 0, width: '2px', height: '100%', background: 'var(--theme-color)', boxShadow: '0 0 15px var(--theme-color)', animation: 'scanning 4s linear infinite' }} />
          </div>

          <div style={{ textAlign: 'center', padding: '20px' }}>
             <div style={{ fontSize: '0.6rem', letterSpacing: '4px', opacity: 0.4, marginBottom: '10px' }}>CURRENTLY_INSPECTING</div>
             <div style={{ fontSize: '1.2rem', fontWeight: 900, textTransform: 'uppercase' }}>{prediction?.trackName || 'NO_TRACK_LOADED'}</div>
          </div>
        </div>

        {/* --- RIGHT: PROTOCOLS --- */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
          <div className="glass-panel" style={{ flex: 1, padding: '20px', background: 'rgba(0,0,0,0.3)', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
            <h3 style={{ fontSize: '0.65rem', letterSpacing: '2px', opacity: 0.5, marginBottom: '15px' }}>EVENT_PROTOCOL</h3>
            <div ref={logTerminalRef} style={{ flex: 1, overflowY: 'auto', fontSize: '0.65rem', fontFamily: 'monospace', color: 'rgba(255,255,255,0.4)', lineHeight: 2.2 }}>
              {logs.map((log, i) => <div key={i} style={{ color: log.includes('RESULT') || log.includes('SCORE') ? 'var(--theme-color)' : 'inherit' }}>{log}</div>)}
            </div>
          </div>
          <div className="glass-panel" style={{ padding: '20px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.1)' }}>
              <div style={{ fontSize: '0.7rem', fontWeight: 900, letterSpacing: '2px', marginBottom: '10px' }}>PREDICTION_CONSENSUS</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 900, color: 'var(--theme-color)' }}>{prediction ? `${prediction.probability}%` : '0.0%'}</div>
              <div style={{ fontSize: '0.6rem', opacity: 0.6, marginTop: '5px' }}>{prediction ? (prediction.isHit ? 'HIT_CONFIDENCE' : 'FLOP_CONFIDENCE') : 'DORMANT'}</div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes scanning { from { left: 0; } to { left: 100%; } }
        @keyframes waveHeight { from { height: 10%; } to { height: 90%; } }
        @keyframes fadeIn { from { opacity: 0; transform: scale(1.02); } to { opacity: 1; transform: scale(1); } }
      `}</style>
    </div>
  );
};

export default DNAVisualizer;
