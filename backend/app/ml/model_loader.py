"""
Model Loader and Inference Service for FastAPI.
Loads the trained Proposed Expense-Aware Hybrid Classifier and handles real-time inference.
"""

import os
import re
from datetime import datetime
import joblib
import numpy as np
import pandas as pd


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class MLModelManager:
    def __init__(self, models_dir: str = None):
        if models_dir is None:
            # Default relative to backend directory or root
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml/models"))
            if not os.path.exists(base_dir):
                base_dir = os.path.abspath("ml/models")
            self.models_dir = base_dir
        else:
            self.models_dir = models_dir

        self.proposed_model = None
        self.load_model()

    def load_model(self):
        model_path = os.path.join(self.models_dir, "proposed_model.pkl")
        if os.path.exists(model_path):
            try:
                self.proposed_model = joblib.load(model_path)
                print(f"[MLModelManager] Loaded proposed model from {model_path}")
            except Exception as e:
                print(f"[MLModelManager] Error loading model from {model_path}: {e}")
                self.proposed_model = None
        else:
            print(f"[MLModelManager] Model file not found at {model_path}")

    def predict_category(
        self,
        description: str,
        amount: float,
        merchant: str = None,
        payment_method: str = "UPI",
        transaction_date: str = None
    ):
        """Perform real ML inference using the trained Proposed Expense-Aware Hybrid Classifier."""
        if self.proposed_model is None:
            self.load_model()
            if self.proposed_model is None:
                raise RuntimeError("ML model is unavailable on the server.")

        # Determine date features
        try:
            if transaction_date:
                dt = datetime.strptime(transaction_date[:10], "%Y-%m-%d")
            else:
                dt = datetime.now()
        except Exception:
            dt = datetime.now()

        # Clean text
        clean_desc = clean_text(description)

        # Build feature DataFrame matching trained schema
        input_data = pd.DataFrame([{
            "clean_description": clean_desc,
            "amount": float(amount),
            "merchant": merchant if merchant else "Unknown",
            "payment_method": payment_method if payment_method else "UPI",
            "day_of_week": dt.weekday(),
            "day_of_month": dt.day,
            "month": dt.month
        }])

        # Inference
        predicted_category = self.proposed_model.predict(input_data)[0]

        # Probabilities & Confidence
        confidence = 0.95
        prob_dict = {}
        if hasattr(self.proposed_model, "predict_proba"):
            probs = self.proposed_model.predict_proba(input_data)[0]
            classes = self.proposed_model.classes_
            for cls_name, prob in zip(classes, probs):
                prob_dict[cls_name] = round(float(prob), 4)
            confidence = round(float(np.max(probs)), 4)

        return {
            "category": str(predicted_category),
            "confidence": confidence,
            "model_name": "Proposed Expense-Aware Hybrid Classifier",
            "probabilities": prob_dict
        }


# Global singleton instance
ml_manager = MLModelManager()
