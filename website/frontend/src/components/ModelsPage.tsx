import { useState } from 'react';

const ModelsPage = ({ sortKey, setSortKey, isFirstTime }: any) => {
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [shouldAnimate] = useState(isFirstTime);

  const initialModels = [
    { name: 'Multi-Vote Model', accuracy: 84.50, f1: 89.20, precision: 86.4, recall: 92.1, status: 'Supreme' },
    { name: 'XGBoost', accuracy: 81.30, f1: 86.10, precision: 83.2, recall: 89.4, status: 'Winner' },
    { name: 'AdaBoost', accuracy: 78.40, f1: 83.50, precision: 80.5, recall: 86.8, status: 'Stable' },
    { name: 'KNN', accuracy: 76.20, f1: 81.00, precision: 78.1, recall: 84.2, status: 'Standard' },
    { name: 'Decision Tree', accuracy: 72.10, f1: 78.40, precision: 75.4, recall: 81.6, status: 'Classic' },
    { name: 'Random Forest', accuracy: 70.40, f1: 76.90, precision: 73.8, recall: 80.2, status: 'Baseline' }
  ];

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

  return (
    <section className={`hero ${shouldAnimate ? 'animate-in' : ''}`} style={{ minHeight: '100vh', height: 'auto', padding: '120px 0 0' }}>
      <div className="container">
        <div className={shouldAnimate ? 'animate-in delay-1' : ''}>
          <h1>Model <span>Performance</span></h1>
          <p>Comparison of our 6 benchmarking algorithms (voted-ensemble system) used to decode the DNA of musical success.</p>
        </div>
        
        <div className={shouldAnimate ? 'animate-in delay-2' : ''} style={{ 
          display: 'flex', justifyContent: 'flex-start', width: '100%', maxWidth: '1000px', 
          marginTop: '4rem', marginBottom: '1.5rem', gap: '1rem', alignItems: 'center'
        }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', fontWeight: 600, textTransform: 'uppercase' }}>Compare Raw Data:</span>
          <select 
            className="brand-input" 
            value={sortKey}
            onChange={(e) => handleSort(e.target.value)}
            style={{ width: 'auto', padding: '0.25rem 1rem', fontSize: '0.85rem' }}
          >
            <option value="accuracy">Accuracy Score</option>
            <option value="f1">F1 Metric</option>
            <option value="precision">Precision (Hits)</option>
            <option value="recall">Recall (Captures)</option>
          </select>
        </div>

        <div className={`glass-panel ${shouldAnimate ? 'animate-in delay-3' : ''}`} style={{ maxWidth: '1000px', marginBottom: '4rem' }}>
          <table className="performance-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('name')} style={{ cursor: 'pointer' }}>
                  ALGORITHM {sortKey === 'name' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('accuracy')} style={{ cursor: 'pointer' }}>
                  ACCURACY {sortKey === 'accuracy' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('f1')} style={{ cursor: 'pointer' }}>
                  F1 SCORE {sortKey === 'f1' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('precision')} style={{ cursor: 'pointer' }}>
                  PRECISION {sortKey === 'precision' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('recall')} style={{ cursor: 'pointer' }}>
                  RECALL {sortKey === 'recall' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th>RANKING</th>
              </tr>
            </thead>
            <tbody>
              {sortedModels.map((model: any) => (
                <tr key={model.name} className="perf-row">
                  <td><strong>{model.name}</strong></td>
                  <td>{(model.accuracy / 100).toFixed(3)}</td>
                  <td>{(model.f1 / 100).toFixed(3)}</td>
                  <td>{(model.precision / 100).toFixed(3)}</td>
                  <td>{(model.recall / 100).toFixed(3)}</td>
                  <td><span className="status-tag">{model.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className={`glass-panel ${shouldAnimate ? 'animate-in delay-4' : ''}`} style={{ marginBottom: '4rem', width: '100%', maxWidth: '1000px' }}>
          <h3 style={{ color: 'var(--brand-green)', marginBottom: '1.5rem', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '2px' }}>
            Visual Benchmarking: {sortKey.toUpperCase()}
          </h3>
          <div className="bar-chart-container" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {sortedModels.map((model: any) => (
              <div key={`chart-${model.name}`} className="bar-row" style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                <div style={{ minWidth: '150px', fontSize: '0.85rem', fontWeight: 600 }}>{model.name}</div>
                <div style={{ flex: 1, height: '12px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px', overflow: 'hidden' }}>
                  <div 
                    style={{ 
                      width: `${model[sortKey]}%`, 
                      height: '100%', 
                      background: model.name === 'SVM' ? 'var(--brand-green)' : 'rgba(255,255,255,0.3)',
                      transition: 'width 1s cubic-bezier(0.2, 0.8, 0.2, 1)',
                      boxShadow: model.name === 'SVM' ? '0 0 15px rgba(29, 185, 84, 0.4)' : 'none'
                    }} 
                  />
                </div>
                <div style={{ minWidth: '60px', textAlign: 'right', fontSize: '0.85rem', color: model.name === 'SVM' ? 'var(--brand-green)' : 'inherit' }}>
                  {(model[sortKey] / 100).toFixed(3)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ModelsPage;
