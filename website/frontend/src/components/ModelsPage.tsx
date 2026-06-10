import { useState } from 'react';

const ModelsPage = ({ sortKey, setSortKey, isFirstTime }: any) => {
  /* --- LOCAL STATE & DATA CONFIGURATION --- */
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [shouldAnimate] = useState(isFirstTime);

  const initialModels = [
    { name: 'Random Forest', accuracy: 78.94, f1: 79.71, precision: 76.91, recall: 82.73, status: 'Top Model' },
    { name: 'Multi Vote Model', accuracy: 71.70, f1: 72.11, precision: 71.07, recall: 73.19, status: 'Consensus' },
    { name: 'KNN', accuracy: 68.84, f1: 68.07, precision: 69.79, recall: 66.44, status: 'Balanced' },
    { name: 'XGBoost', accuracy: 68.76, f1: 69.38, precision: 68.04, recall: 70.77, status: 'Strong' },
    { name: 'Decision Tree', accuracy: 62.26, f1: 62.89, precision: 61.86, recall: 63.96, status: 'Classic' },
    { name: 'AdaBoost', accuracy: 55.88, f1: 56.88, precision: 55.62, recall: 58.20, status: 'Weakest' }
  ];

  /* --- DATA SORTING LOGIC --- */
  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('desc');
    }
  };

  const sortedModels = [...initialModels].sort((a: any, b: any) => {
    const aVal = a[sortKey];
    const bVal = b[sortKey];
    if (typeof aVal === 'string') {
      return sortOrder === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
    return sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
  });

  // Highlight the best-performing model (highest accuracy), not a hardcoded one.
  const topModel = [...initialModels].sort((a, b) => b.accuracy - a.accuracy)[0].name;

  return (
    <section className={`hero ${shouldAnimate ? 'animate-in' : ''}`} style={{ 
      minHeight: '100vh', height: 'auto', padding: '140px 0 100px', display: 'flex', flexDirection: 'column' 
    }}>
      <div className="container" style={{ maxWidth: '1400px', display: 'flex', flexDirection: 'column', flex: 1 }}>
        
        {/* --- HEADER ANALYTICS SECTION --- */}
        <div className={shouldAnimate ? 'animate-in' : ''} style={{ textAlign: 'center', marginBottom: '5rem' }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '1.5rem' }}>Model <span>Precision</span></h1>
          <p style={{ margin: '0 auto', opacity: 0.7, fontSize: '1rem', maxWidth: '750px', lineHeight: '1.8' }}>
            Benchmarking our optimized ensemble intelligence against 50,768 balanced samples.
            Utilizing a low-bias popularity threshold optimized to detect emerging independent hits and local chart-toppers.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: '3rem', flex: 1 }}>
          
          {/* --- BENCHMARK DATA TABLE --- */}
          <div className={`glass-panel ${shouldAnimate ? 'animate-in delay-1' : ''}`} style={{ 
            padding: '0', background: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.05)', overflow: 'hidden'
          }}>
            <table className="performance-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid rgba(255,255,255,0.07)' }}>
                  <th onClick={() => handleSort('name')} style={{ padding: '1.4rem 1.8rem', textAlign: 'left', cursor: 'pointer', fontSize: '0.65rem', letterSpacing: '2px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                    Algorithm {sortKey === 'name' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('accuracy')} style={{ padding: '1rem', textAlign: 'center', cursor: 'pointer', fontSize: '0.65rem', letterSpacing: '2px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                    Accuracy {sortKey === 'accuracy' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('f1')} style={{ padding: '1rem', textAlign: 'center', cursor: 'pointer', fontSize: '0.65rem', letterSpacing: '2px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                    F1 Score {sortKey === 'f1' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th style={{ padding: '1.4rem 1.8rem', textAlign: 'right', fontSize: '0.65rem', letterSpacing: '2px', color: 'var(--text-dim)' }}>RANK</th>
                </tr>
              </thead>
              <tbody>
                {sortedModels.map((model: any, idx: number) => (
                  <tr key={model.name} className="perf-row" style={{ 
                    borderBottom: '1px solid rgba(255,255,255,0.03)',
                    background: model.name === topModel ? 'rgba(255,255,255,0.02)' : 'transparent'
                  }}>
                    <td style={{ padding: '1.1rem 1.8rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <span style={{ fontSize: '0.75rem', opacity: 0.2 }}>{idx + 1}</span>
                        <strong style={{ fontSize: '1rem', color: model.name === topModel ? 'var(--theme-color)' : 'white' }}>{model.name}</strong>
                      </div>
                    </td>
                    <td style={{ textAlign: 'center', fontSize: '1rem', fontWeight: 600 }}>{(model.accuracy / 100).toFixed(3)}</td>
                    <td style={{ textAlign: 'center', fontSize: '1rem', opacity: 0.6 }}>{(model.f1 / 100).toFixed(3)}</td>
                    <td style={{ padding: '1.1rem 1.8rem', textAlign: 'right' }}>
                      <span className="status-tag" style={{ border: model.name === topModel ? '1px solid var(--theme-color)' : '1px solid rgba(255,255,255,0.1)' }}>
                        {model.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* --- ANALYTIC VISUALIZATION MODULES --- */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            
            <div className={`glass-panel ${shouldAnimate ? 'animate-in delay-2' : ''}`} style={{ flex: 1, padding: '2rem', background: 'rgba(255,255,255,0.01)' }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2rem' }}>
                <h3 style={{ fontSize: '0.75rem', letterSpacing: '3px', textTransform: 'uppercase', color: 'white', margin: 0 }}>
                  Benchmark Analytics
                </h3>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {sortedModels.map((model: any) => (
                  <div key={`chart-${model.name}`}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.85rem' }}>
                      <span style={{ fontWeight: 600, opacity: 0.8 }}>{model.name}</span>
                      <span style={{ color: model.name === topModel ? 'var(--theme-color)' : 'white', fontWeight: 900 }}>{model.accuracy}%</span>
                    </div>
                    <div style={{ height: '5px', background: 'rgba(255,255,255,0.03)', borderRadius: '3px', overflow: 'hidden' }}>
                      <div 
                        style={{ 
                          width: `${model.accuracy}%`, height: '100%', 
                          background: model.name === topModel ? 'var(--theme-color)' : 'rgba(255,255,255,0.2)',
                          borderRadius: '3px', transition: 'width 2s cubic-bezier(0,0.8,0.2,1)',
                          boxShadow: model.name === topModel ? '0 0 15px var(--theme-color-faded)' : 'none'
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* --- RELIABILITY SCOREBOARD --- */}
            <div className={`glass-panel ${shouldAnimate ? 'animate-in delay-3' : ''}`} style={{ 
              padding: '2rem 3rem', display: 'flex', alignItems: 'center', gap: '3rem',
              background: 'rgba(0,0,0,0.2)', border: '1px solid rgba(255,255,255,0.05)'
            }}>
              <div style={{ position: 'relative', width: '130px', height: '130px', flexShrink: 0 }}>
                <svg viewBox="0 0 100 100" style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
                  <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="0.5" />
                  <circle 
                    cx="50" cy="50" r="45" fill="none" 
                    stroke="var(--theme-color)" strokeWidth="4" strokeDasharray="282.7"
                    strokeDashoffset={282.7 * (1 - 0.797)} strokeLinecap="round"
                    style={{ transition: 'stroke-dashoffset 2.5s ease-out' }}
                  />
                </svg>
                <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center' }}>
                  <div style={{ fontSize: '2.1rem', fontWeight: 900, lineHeight: 1 }}>.797</div>
                  <div style={{ fontSize: '0.6rem', letterSpacing: '1.5px', opacity: 0.5, marginTop: '3px' }}>F1 SCORE</div>
                </div>
              </div>
              <div>
                <h4 style={{ fontSize: '0.8rem', letterSpacing: '2px', textTransform: 'uppercase', color: 'white', marginBottom: '0.8rem' }}>Data Reliability</h4>
                <p style={{ fontSize: '0.8rem', opacity: 0.5, margin: 0, lineHeight: 1.6 }}>
                  Our analytics suite ensures consistent audio metric interpretation across 50,768 balanced diverse samples.
                  Minimizing variance through ensemble voting.
                </p>
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>
  );
};

export default ModelsPage;
