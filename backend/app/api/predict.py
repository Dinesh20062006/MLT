from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.prediction_log import PredictionLog
from backend.app.schemas.prediction import PredictionRequest, PredictionResponse
from backend.app.ml.model_loader import ml_manager
from backend.app.utils.auth import get_current_user

router = APIRouter(tags=["Machine Learning Prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict_expense_category(
    req: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict expense category using the Proposed Expense-Aware Hybrid Classifier.
    Transforms description and structured features (amount, merchant, payment method, date)
    into the hybrid feature space and returns predicted category with probabilistic confidence.
    """
    if not req.description or not req.description.strip():
        raise HTTPException(status_code=400, detail="Transaction description cannot be empty.")
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Transaction amount must be greater than zero.")

    try:
        prediction_result = ml_manager.predict_category(
            description=req.description,
            amount=req.amount,
            merchant=req.merchant,
            payment_method=req.payment_method,
            transaction_date=req.transaction_date
        )

        # Log prediction to Oracle PREDICTION_LOGS
        log_entry = PredictionLog(
            user_id=current_user.user_id if current_user else None,
            input_description=req.description[:255],
            input_amount=req.amount,
            predicted_category=prediction_result["category"],
            confidence=prediction_result["confidence"],
            model_name=prediction_result["model_name"]
        )
        db.add(log_entry)
        db.commit()

        return prediction_result

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
