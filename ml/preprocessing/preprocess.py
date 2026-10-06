"""
Data Preprocessing and Feature Extraction for Smart Expense Classification.
Handles text cleaning, tokenization, feature transformation, and train/test splitting.
"""

import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42
TEST_SIZE = 0.20


def clean_text(text: str) -> str:
    """Preprocess transaction text by lowercasing, removing special characters, and normalizing."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_and_split_data(csv_path: str = "ml/data/expense_dataset.csv"):
    """Load expense dataset, add derived features, and split 80/20 with random_state=42."""
    df = pd.read_csv(csv_path)

    # Clean text description
    df["clean_description"] = df["description"].apply(clean_text)

    # Date-derived features
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["day_of_week"] = df["transaction_date"].dt.dayofweek
    df["day_of_month"] = df["transaction_date"].dt.day
    df["month"] = df["transaction_date"].dt.month

    # Stratified 80/20 split
    X = df[["clean_description", "amount", "merchant", "payment_method", "day_of_week", "day_of_month", "month"]]
    y = df["category"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    return X_train, X_test, y_train, y_test


def build_text_vectorizer():
    """Build TF-IDF vectorizer for baseline text-only models."""
    return TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
        stop_words="english"
    )


def build_hybrid_preprocessor():
    """Build ColumnTransformer for Proposed Expense-Aware Hybrid Classifier.
    Combines:
    1. Text Features: TF-IDF of transaction description
    2. Numerical Features: Log-transformed and scaled transaction amount
    3. Categorical Features: One-hot encoded merchant and payment method
    4. Temporal Features: Day of week, day of month, month scaled
    """
    text_transformer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=4000,
        sublinear_tf=True,
        stop_words="english"
    )

    num_transformer = Pipeline([
        ("log", FunctionTransformer(np.log1p, validate=False)),
        ("scaler", StandardScaler(with_mean=False))
    ])

    date_transformer = StandardScaler(with_mean=False)

    cat_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("text", text_transformer, "clean_description"),
            ("num", num_transformer, ["amount"]),
            ("cat", cat_transformer, ["merchant", "payment_method"]),
            ("date", date_transformer, ["day_of_week", "day_of_month", "month"])
        ],
        remainder="drop"
    )

    return preprocessor
