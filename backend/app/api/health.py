from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database.session import get_db
from backend.app.ml.model_loader import ml_manager

router = APIRouter(prefix="/health", tags=["Health & Status"])


@router.get("")
def health_check(db: Session = Depends(get_db)):
    oracle_status = "ok"
    try:
        db.execute(text("SELECT 1 FROM DUAL"))
    except Exception as e:
        oracle_status = f"unhealthy: {str(e)}"

    ml_status = "ok" if ml_manager.proposed_model is not None else "model_not_loaded"

    return {
        "status": "healthy" if oracle_status == "ok" and ml_status == "ok" else "degraded",
        "oracle_database": oracle_status,
        "ml_model_loaded": ml_status,
        "system": "Smart Expense Category Prediction & Financial Analytics API"
    }
