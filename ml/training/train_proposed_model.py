"""
Training script for the Proposed Expense-Aware Hybrid Classifier.
Academic Innovation:
Fuses unstructured textual signals (TF-IDF n-grams) with structured financial features
(log-normalized amount, categorical merchant & payment method, temporal calendar attributes)
through a unified ColumnTransformer into an optimized multi-modal hybrid classifier
with calibrated probabilistic confidence estimation.
"""

import os
import sys
import time
import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ml.preprocessing.preprocess import load_and_split_data, build_hybrid_preprocessor


def train_proposed_model(models_dir: str = "ml/models"):
    os.makedirs(models_dir, exist_ok=True)

    print("Loading dataset for Proposed Expense-Aware Hybrid Classifier training...")
    X_train, X_test, y_train, y_test = load_and_split_data()

    print(f"Training split: {len(X_train)} samples | Test split: {len(X_test)} samples")

    preprocessor = build_hybrid_preprocessor()

    # The proposed classifier leverages the combined sparse-dense feature space
    # with SAGA solver for multi-class cross-entropy
    classifier = LogisticRegression(
        C=2.5,
        max_iter=1500,
        solver="saga",
        random_state=42
    )

    proposed_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    print("\n--- Training Proposed Expense-Aware Hybrid Classifier ---")
    t0 = time.time()
    proposed_pipeline.fit(X_train, y_train)
    duration = time.time() - t0
    print(f"Proposed Model trained in {duration:.2f} seconds")

    model_path = os.path.join(models_dir, "proposed_model.pkl")
    joblib.dump(proposed_pipeline, model_path)
    print(f"Saved {model_path}")

    return proposed_pipeline, duration


if __name__ == "__main__":
    train_proposed_model()
