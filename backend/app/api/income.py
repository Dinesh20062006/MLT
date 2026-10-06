from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.income import Income
from backend.app.schemas.income import IncomeCreateOrUpdate, IncomeResponse
from backend.app.utils.auth import get_current_user

router = APIRouter(prefix="/income", tags=["Salary & Income"])


@router.get("", response_model=IncomeResponse)
def get_user_income(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    income = db.query(Income).filter(Income.user_id == current_user.user_id).first()
    if not income:
        # Default income if none set
        income = Income(user_id=current_user.user_id, monthly_income=0.0)
        db.add(income)
        db.commit()
        db.refresh(income)
    return income


@router.post("", response_model=IncomeResponse)
def set_or_update_income(
    income_in: IncomeCreateOrUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if income_in.monthly_income < 0:
        raise HTTPException(status_code=400, detail="Monthly income cannot be negative.")

    income = db.query(Income).filter(Income.user_id == current_user.user_id).first()
    if income:
        income.monthly_income = income_in.monthly_income
    else:
        income = Income(user_id=current_user.user_id, monthly_income=income_in.monthly_income)
        db.add(income)

    db.commit()
    db.refresh(income)
    return income
