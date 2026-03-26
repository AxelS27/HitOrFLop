# 🎵 Music Hit Predictor

Full-stack machine learning application to predict if a song will be a hit on Spotify based on its acoustic characteristics.

## 📁 Project Structure

- `model_training/`: Data science pipeline, CSV datasets, and Jupyter notebook.
- `website/`: Production application.
  - `backend/`: FastAPI Python server for model inference and audio analysis.
  - `frontend/`: React + Vite frontend with premium Spotify-inspired design.

## 🚀 Getting Started

### 1. Backend Setup (Python)
Navigate to `website/backend`:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
python main.py
```
*Note: Ensure trained `.pkl` models from `model_training/models` are copied to `website/backend/models/` (this is already done).*

### 2. Frontend Setup (React)
Navigate to `website/frontend`:
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

## 🛠️ Tech Stack
- **Frontend**: React, TypeScript, Tailwind CSS, Framer Motion.
- **Backend**: FastAPI, Scikit-learn, XGBoost, Librosa.
- **Models**: Logistic Regression, KNN, SVM, Random Forest, XGBoost.

## 🧪 How to Use
1. Paste a **Spotify Link** or **Upload an MP3/WAV file**.
2. Select your preferred **AI Model**.
3. View the **Hit Probability** and detailed **Model Analytical Deep-dive**.
