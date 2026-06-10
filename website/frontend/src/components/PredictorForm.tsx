import { useState } from 'react';

const PredictorForm = ({ onStart, onResult }: any) => {
  const [model, setModel] = useState('Multi Vote Model');
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handlePredict = async () => {
    onStart();
    
    const formData = new FormData();
    formData.append('model_name', model);
    if (file) {
      formData.append('file', file);
    } else if (isLinkValid) {
      formData.append('youtube_url', youtubeUrl);
    }

    // Abort if the backend (HF Space) is asleep/too slow, so the UI never hangs forever.
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000); // 120s

    try {
      const response = await fetch('https://axels27-music-hit-predictor-api.hf.space/predict', {
        method: 'POST',
        mode: 'cors',
        body: formData,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Backend Error Response:', errorText);
        throw new Error(`Backend Error (${response.status}): ${errorText.substring(0, 50)}...`);
      }
      
      const resultData = await response.json();
      onResult(resultData);
    } catch (err: any) {
      clearTimeout(timeoutId);
      console.error(err);
      const msg = err.name === 'AbortError'
        ? 'Server took too long to respond (the analysis engine may be waking up). Please try again in a moment.'
        : err.message;
      alert(`Backend Error: ${msg}\n\nFalling back to Demo Mode for visualization.`);
      
      onResult({
        isHit: true,
        model: `${model} (Demo Mode)`,
        probability: 92.4,
        analysis: [
          { feature: 'Energy', value: '0.82', impact: 'High energy characteristic' },
          { feature: 'Tempo', value: '121 BPM', impact: 'Strong rhythm presence' },
          { feature: 'Confidence', value: '88%', impact: 'Model certainty' }
        ]
      });
    }
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => {
    setIsDragging(false);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && (droppedFile.name.endsWith('.mp3') || droppedFile.name.endsWith('.wav'))) {
      setFile(droppedFile);
    }
  };

  const isLinkValid = youtubeUrl.trim().includes('youtube.com/') || youtubeUrl.trim().includes('youtu.be/');
  const isFileValid = file !== null && (file.name.endsWith('.mp3') || file.name.endsWith('.wav'));
  const canAnalyze = isFileValid || isLinkValid;

  return (
    <div className="glass-panel" style={{ alignSelf: 'center', marginTop: '2rem' }}>
      <div className="input-group">
        <label className="input-label">1. Choose AI Model</label>
        <select 
          className="brand-input" 
          value={model}
          onChange={(e) => setModel(e.target.value)}
        >
          <option value="Multi Vote Model">Multi Vote Model (Voted Ensemble)</option>
          <option value="XGBoost">XGBoost (High Accuracy)</option>
          <option value="Random Forest">Random Forest</option>
          <option value="AdaBoost">AdaBoost</option>
          <option value="KNN">KNN</option>
          <option value="Decision Tree">Decision Tree</option>
        </select>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 0.1fr 1fr', gap: '1rem', alignItems: 'center' }}>
        <div className="input-group">
          <label className="input-label">2a. Upload MP3/WAV</label>
          <div 
            className={`file-upload-area ${isDragging ? 'dragging' : ''}`}
            onClick={() => document.getElementById('audio-up')?.click()}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
          >
            <input 
              id="audio-up" 
              type="file" 
              hidden 
              accept=".mp3,.wav" 
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            {file ? <div style={{ color: 'var(--brand-green)' }}>{file.name}</div> : <div style={{ color: 'white' }}>Drag or click to browse</div>}
            <div style={{ fontSize: '0.7rem', color: '#b3b3b3', marginTop: '0.5rem' }}>MAX 10MB</div>
          </div>
        </div>

        <div style={{ color: '#b3b3b3', fontStyle: 'italic', fontSize: '0.8rem' }}>OR</div>

        <div className="input-group">
          <label className="input-label">2b. Paste YouTube Link</label>
          <input 
            className="brand-input" 
            placeholder="youtube.com/watch?v=..."
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
          />
          <div style={{ fontSize: '0.7rem', color: '#b3b3b3', marginTop: '0.5rem' }}>INSTANT YOUTUBE ANALYSIS</div>
        </div>
      </div>

      {canAnalyze && (
        <button className="btn-primary" onClick={handlePredict} style={{ marginTop: '2.5rem', width: '100%', animation: 'slideUp 0.4s ease-out' }}>
          ANALYZE THIS TRACK
        </button>
      )}
    </div>
  );
};

export default PredictorForm;
