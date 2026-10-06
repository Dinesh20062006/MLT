from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class ModelMetric(BaseModel):
    name: str
    type: str  # 'baseline' or 'proposed'
    description: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    training_time: float
    inference_time: float
    per_category: Optional[Dict[str, Dict[str, float]]] = None
    confusion_matrix: Optional[List[List[int]]] = None


class ModelComparisonSummary(BaseModel):
    best_model_key: str
    best_model_name: str
    best_f1: float
    best_accuracy: float
    classes: List[str]
    test_samples: int
    comparison_with_rf: Dict[str, Any]


class ModelComparisonResponse(BaseModel):
    models: Dict[str, ModelMetric]
    summary: ModelComparisonSummary
