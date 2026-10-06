from typing import List, Dict, Optional
from pydantic import BaseModel


class CategoryExpenseItem(BaseModel):
    category: str
    amount: float
    percentage: float
    count: int
    color_hex: Optional[str] = "#2563EB"


class MonthlyTrendItem(BaseModel):
    month: str
    income: float
    expenses: float
    savings: float


class FinancialOverview(BaseModel):
    # Monthly
    monthly_income: float
    monthly_expenses: float
    monthly_savings: float
    savings_rate: float

    # Annual
    annual_income: float
    annual_expenses: float
    annual_savings: float

    # Weekly Estimates
    estimated_weekly_income: float
    estimated_weekly_expenses: float
    estimated_weekly_savings: float

    # Summary Stats
    total_lifetime_expenses: float
    average_expense_amount: float
    highest_expense_amount: float
    most_used_category: Optional[str] = None
    total_transaction_count: int


class DashboardAnalyticsResponse(BaseModel):
    overview: FinancialOverview
    category_distribution: List[CategoryExpenseItem]
    monthly_trend: List[MonthlyTrendItem]
    has_salary_configured: bool


class WeeklyAnalyticsResponse(BaseModel):
    estimated_weekly_income: float
    estimated_weekly_expenses: float
    estimated_weekly_savings: float
    note: str = "Estimated Weekly calculations are derived using Annual values divided by 52 weeks."


class MonthlyAnalyticsResponse(BaseModel):
    monthly_income: float
    monthly_expenses: float
    monthly_savings: float
    savings_rate: float
    monthly_trend: List[MonthlyTrendItem]


class AnnualAnalyticsResponse(BaseModel):
    annual_income: float
    annual_expenses: float
    annual_savings: float
    projected_savings_rate: float
    note: str = "Annual values represent 12x monthly projections and annualized tracking."
