import os
import json
from fastapi import APIRouter, HTTPException
from backend.app.schemas.model_comparison import ModelComparisonResponse

router = APIRouter(prefix="/model-comparison", tags=["Model Comparison"])


@router.get("", response_model=ModelComparisonResponse)
def get_model_comparison_results():
    """Returns actual ML evaluation metrics generated from experimental training.
    NO HARDCODED OR FAKE RESULTS.
    """
    results_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../ml/evaluation/results.json")
    )
    if not os.path.exists(results_path):
        results_path = os.path.abspath("ml/evaluation/results.json")

    if not os.path.exists(results_path):
        raise HTTPException(
            status_code=404,
            detail="Model evaluation results not found. Please run ml/evaluation/evaluate_models.py first."
        )

    try:
        with open(results_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read evaluation results: {str(e)}")
