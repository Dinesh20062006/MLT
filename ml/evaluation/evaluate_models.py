"""
Model Evaluation Pipeline for Smart Expense Category Prediction.
Evaluates all four models on the exact same 20% test split:
1. Logistic Regression (Baseline 1)
2. Decision Tree Classifier (Baseline 2)
3. Random Forest Classifier (Baseline 3)
4. Proposed Expense-Aware Hybrid Classifier

Computes real evaluation metrics:
- Accuracy
- Macro Precision
- Macro Recall
- Macro F1-score
- Confusion Matrix
- Category-wise metrics
- Training times

Saves actual experimental results to ml/evaluation/results.json.
NO HARDCODED OR FAKE METRICS.
"""

import os
import sys
import json
import time
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ml.preprocessing.preprocess import load_and_split_data
from ml.training.train_baselines import train_baselines
from ml.training.train_proposed_model import train_proposed_model


def run_full_evaluation(models_dir: str = "ml/models", eval_dir: str = "ml/evaluation"):
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)

    print("=" * 65)
    print("STEP 1: Training Baselines and Proposed Model")
    print("=" * 65)

    # Train baselines
    baseline_results = train_baselines(models_dir)

    # Train proposed model
    proposed_pipeline, proposed_train_time = train_proposed_model(models_dir)

    print("\n" + "=" * 65)
    print("STEP 2: Evaluating All Four Models on the Same 20% Test Split")
    print("=" * 65)

    X_train, X_test, y_train, y_test = load_and_split_data()
    classes = sorted(list(y_test.unique()))

    # Load vectorizer for baselines
    tfidf = joblib.load(os.path.join(models_dir, "tfidf_vectorizer.pkl"))
    X_test_tfidf = tfidf.transform(X_test["clean_description"])

    # Load models
    models = {
        "logistic_regression": {
            "name": "Logistic Regression",
            "model": joblib.load(os.path.join(models_dir, "logistic_regression.pkl")),
            "X_test": X_test_tfidf,
            "train_time": baseline_results["logistic_regression"][1],
            "type": "baseline",
            "description": "Linear classification baseline that predicts probability distribution over expense categories using text TF-IDF representations."
        },
        "decision_tree": {
            "name": "Decision Tree Classifier",
            "model": joblib.load(os.path.join(models_dir, "decision_tree.pkl")),
            "X_test": X_test_tfidf,
            "train_time": baseline_results["decision_tree"][1],
            "type": "baseline",
            "description": "Non-linear tree baseline that partitions text feature space using orthogonal decision boundaries."
        },
        "random_forest": {
            "name": "Random Forest Classifier",
            "model": joblib.load(os.path.join(models_dir, "random_forest.pkl")),
            "X_test": X_test_tfidf,
            "train_time": baseline_results["random_forest"][1],
            "type": "baseline",
            "description": "Ensemble of decorrelated decision trees combining bootstrap aggregated subsets for enhanced generalization."
        },
        "proposed_hybrid": {
            "name": "Proposed Expense-Aware Hybrid Classifier",
            "model": proposed_pipeline,
            "X_test": X_test,  # Takes structured dataframe directly through ColumnTransformer
            "train_time": proposed_train_time,
            "type": "proposed",
            "description": "Novel multi-modal classifier combining sublinear TF-IDF text features with structured transaction features (log amount, merchant, payment method, temporal calendar attributes)."
        }
    }

    results = {}
    print(f"\nEvaluating on {len(y_test)} unseen test samples across {len(classes)} categories...\n")

    for key, item in models.items():
        m = item["model"]
        X_eval = item["X_test"]

        t_infer_start = time.time()
        y_pred = m.predict(X_eval)
        infer_time = time.time() - t_infer_start

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
        rec = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
        f1 = float(f1_score(y_test, y_pred, average="macro", zero_division=0))

        cm = confusion_matrix(y_test, y_pred, labels=classes).tolist()
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

        # Per-category metrics
        per_category = {}
        for cat in classes:
            if cat in report:
                per_category[cat] = {
                    "precision": round(float(report[cat]["precision"]), 4),
                    "recall": round(float(report[cat]["recall"]), 4),
                    "f1": round(float(report[cat]["f1-score"]), 4),
                    "support": int(report[cat]["support"])
                }

        results[key] = {
            "name": item["name"],
            "type": item["type"],
            "description": item["description"],
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "training_time": round(float(item["train_time"]), 2),
            "inference_time": round(float(infer_time), 4),
            "per_category": per_category,
            "confusion_matrix": cm
        }

        print(f"{item['name']:<44} | Acc: {acc*100:6.2f}% | Prec: {prec*100:6.2f}% | Rec: {rec*100:6.2f}% | Macro F1: {f1*100:6.2f}% | Time: {item['train_time']:.2f}s")

    # Determine best model dynamically based on real Macro F1
    sorted_by_f1 = sorted(results.items(), key=lambda x: x[1]["f1"], reverse=True)
    best_key, best_data = sorted_by_f1[0]

    rf_f1 = results["random_forest"]["f1"]
    prop_f1 = results["proposed_hybrid"]["f1"]
    diff_f1 = round(prop_f1 - rf_f1, 4)
    pct_diff = round(((prop_f1 - rf_f1) / rf_f1) * 100, 2) if rf_f1 > 0 else 0.0

    summary = {
        "best_model_key": best_key,
        "best_model_name": best_data["name"],
        "best_f1": best_data["f1"],
        "best_accuracy": best_data["accuracy"],
        "classes": classes,
        "test_samples": len(y_test),
        "comparison_with_rf": {
            "proposed_f1": prop_f1,
            "random_forest_f1": rf_f1,
            "f1_difference": diff_f1,
            "percentage_improvement": pct_diff,
            "proposed_outperformed_rf": prop_f1 > rf_f1
        }
    }

    final_payload = {
        "models": results,
        "summary": summary
    }

    results_json_path = os.path.join(eval_dir, "results.json")
    with open(results_json_path, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=4)

    print("\n" + "=" * 65)
    print("RESULTS SAVED TO:", results_json_path)
    print(f"Best Model: {best_data['name']} (Macro F1 = {best_data['f1']:.4f})")
    print(f"Proposed vs Random Forest F1 Diff: {diff_f1:+.4f} ({pct_diff:+.2f}%)")
    print("=" * 65)

    return final_payload


if __name__ == "__main__":
    run_full_evaluation()
