"""
Training script for the three Machine Learning Baseline Models:
1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier

Academic Benchmark:
Trained on TF-IDF textual representation of transaction descriptions.
"""

import os
import sys
import time
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ml.preprocessing.preprocess import load_and_split_data, build_text_vectorizer


def train_baselines(models_dir: str = "ml/models"):
    os.makedirs(models_dir, exist_ok=True)

    print("Loading dataset for baseline training...")
    X_train, X_test, y_train, y_test = load_and_split_data()

    print(f"Training split: {len(X_train)} samples | Test split: {len(X_test)} samples")

    # Fit TF-IDF Vectorizer
    print("Fitting TF-IDF Vectorizer on training descriptions...")
    tfidf = build_text_vectorizer()
    X_train_tfidf = tfidf.fit_transform(X_train["clean_description"])
    joblib.dump(tfidf, os.path.join(models_dir, "tfidf_vectorizer.pkl"))
    print("Saved tfidf_vectorizer.pkl")

    baseline_configs = {
        "logistic_regression": {
            "name": "Logistic Regression",
            "model": LogisticRegression(max_iter=1000, random_state=42)
        },
        "decision_tree": {
            "name": "Decision Tree Classifier",
            "model": DecisionTreeClassifier(max_depth=30, random_state=42)
        },
        "random_forest": {
            "name": "Random Forest Classifier",
            "model": RandomForestClassifier(n_estimators=100, max_depth=30, random_state=42, n_jobs=-1)
        }
    }

    trained_models = {}
    for key, cfg in baseline_configs.items():
        print(f"\n--- Training {cfg['name']} ---")
        t0 = time.time()
        model = cfg["model"]
        model.fit(X_train_tfidf, y_train)
        duration = time.time() - t0
        print(f"Completed in {duration:.2f} seconds")

        model_path = os.path.join(models_dir, f"{key}.pkl")
        joblib.dump(model, model_path)
        print(f"Saved {model_path}")
        trained_models[key] = (model, duration)

    print("\nAll baseline models trained successfully!")
    return trained_models


if __name__ == "__main__":
    train_baselines()
