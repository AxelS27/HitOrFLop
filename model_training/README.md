# Hit or Flop? Benchmarking Traditional ML Models for Spotify Success Prediction

## 1. Project Summary
This project focuses on developing a classification system to predict the success of a song (**"Hit"** vs **"Flop"**) using audio features and metadata. The project specifically utilizes **Traditional Machine Learning** via the `scikit-learn` library to compare the performance of 4 algorithms without using Neural Networks (Deep Learning).

## 2. User Target Analysis
* **Intelligent Systems Students:** Need statistically valid model comparisons and feature analysis.
* **Beginner Data Scientists:** Need clean, modular, and easy-to-interpret end-to-end pipeline examples.

## 3. Technical Specifications
* **Programming Language:** Python 3.x
* **Core Library:** `scikit-learn`
* **Data Manipulation:** `pandas`, `numpy`
* **Signal Processing:** `librosa` (for audio feature extraction from raw files)
* **Visualization:** `seaborn`, `matplotlib`

## 4. Dataset & Feature Engineering
The primary dataset used is from **The Spotify Hit Predictor Dataset (Kaggle)**.

### A. Input Features ($X$)
1.  **Metadata (API-Based):** `danceability`, `energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_ms`, `time_signature`.
2.  **Audio Signals (Engineered via Librosa):**
    * `mfcc_mean`: Representation of sound timbre texture.
    * `spectral_rolloff`: Frequency below which a certain percentage of total spectral energy lies.
3.  **Contextual Data:**
    * `release_decade`: (Added) To analyze audio trend shifts across generations.
    * `artist_follower_count`.

### B. Target Variable ($y$)
* `target`: Binary variable (1 = Hit, 0 = Flop).

## 5. Models Compared
This experiment will compare 4 classic algorithm architectures:

| Model | Type | Advantages | Role |
| :--- | :--- | :--- | :--- |
| **Logistic Regression** | Linear Model | Very fast and easy to interpret (Explainable AI). | Baseline |
| **K-Nearest Neighbors** | Instance-based | Effective if data has strong local patterns. | Similarity Check |
| **Support Vector Machine** | Kernel-based | Very robust for high-dimensional data. | Robustness |
| **Random Forest** | Ensemble Learning | High accuracy, stable, and includes *Feature Importance*. | Performance King |

## 6. System Workflow (Pipeline)
1.  **Data Ingestion:** Loading CSV files resulting from the combination of metadata and audio features.
2.  **Preprocessing & Data Balancing:**
    * Handling missing values using Simple Imputer.
    * Feature Scaling using `StandardScaler()`.
    * **Addressing Class Imbalance:** Using **SMOTE** (Synthetic Minority Over-sampling Technique) or **Stratified Shuffling** to ensure the model is not biased towards "Flop" songs.
3.  **Model Training & Hyperparameter Tuning:**
    * Training the 4 models in parallel.
    * Using **GridSearchCV** or **RandomizedSearchCV** to find optimal parameters for each algorithm.
4.  **Evaluation & Explainable AI (XAI):**
    * Metrics: Accuracy, F1-Score, and Precision/Recall.
    * Visualization: Confusion Matrix and ROC-AUC Plot.
    * **Shapley Additive Explanations (SHAP):** Implementing SHAP to explain specific feature contributions to individual predictions (Local Explainability) and global influence (Global Explainability).
    * **Temporal Analysis:** Visualizing model accuracy per decade to detect *Data Drift*.

## 7. Technical References
The project implementation refers to documentation standards from:
* **Hands-On Machine Learning with Scikit-Learn...** (Geron, A.): For modular pipeline structure.
* **Mastering Machine Learning with scikit-learn** (Hackeling, G.): For hyperparameter tuning techniques.