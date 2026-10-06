from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.schemas.analytics import (
    DashboardAnalyticsResponse,
    WeeklyAnalyticsResponse,
    MonthlyAnalyticsResponse,
    AnnualAnalyticsResponse
)
from backend.app.services.analytics_service import calculate_financial_analytics
from backend.app.utils.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Financial Analytics"])


@router.get("", response_model=DashboardAnalyticsResponse)
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get complete financial overview including monthly, annual, weekly estimates,
    category distributions, and spending trends.
    """
    analytics = calculate_financial_analytics(db, current_user.user_id)
    return analytics


@router.get("/weekly", response_model=WeeklyAnalyticsResponse)
def get_weekly_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get estimated weekly income, expenses, and savings calculated via Annual / 52."""
    analytics = calculate_financial_analytics(db, current_user.user_id)
    ov = analytics["overview"]
    return {
        "estimated_weekly_income": ov["estimated_weekly_income"],
        "estimated_weekly_expenses": ov["estimated_weekly_expenses"],
        "estimated_weekly_savings": ov["estimated_weekly_savings"],
        "note": "Estimated Weekly calculations are derived using Annual values divided by 52 weeks."
    }


@router.get("/monthly", response_model=MonthlyAnalyticsResponse)
def get_monthly_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get monthly financial figures and monthly trend history."""
    analytics = calculate_financial_analytics(db, current_user.user_id)
    ov = analytics["overview"]
    return {
        "monthly_income": ov["monthly_income"],
        "monthly_expenses": ov["monthly_expenses"],
        "monthly_savings": ov["monthly_savings"],
        "savings_rate": ov["savings_rate"],
        "monthly_trend": analytics["monthly_trend"]
    }


@router.get("/annual", response_model=AnnualAnalyticsResponse)
def get_annual_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get annual income, expenses, and savings projections (12x monthly)."""
    analytics = calculate_financial_analytics(db, current_user.user_id)
    ov = analytics["overview"]
    return {
        "annual_income": ov["annual_income"],
        "annual_expenses": ov["annual_expenses"],
        "annual_savings": ov["annual_savings"],
        "projected_savings_rate": ov["savings_rate"],
        "note": "Annual values represent 12x monthly projections and annualized tracking."
    }
