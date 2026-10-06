"""
Financial Analytics Service.
Performs strictly consistent financial calculations:
- Monthly income, expenses, savings, and savings percentage
- Annual income, expenses, and savings projections (12x)
- Estimated Weekly income, expenses, and savings (Annual / 52)
- Category breakdown and monthly trends
- Handles zero income safely without division by zero.
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.income import Income
from backend.app.models.expense import Expense

CATEGORY_COLORS = {
    "Food": "#10B981",
    "Transportation": "#3B82F6",
    "Shopping": "#EC4899",
    "Entertainment": "#8B5CF6",
    "Utilities": "#F59E0B",
    "Healthcare": "#EF4444",
    "Education": "#06B6D4",
    "Other": "#6B7280"
}


def calculate_financial_analytics(db: Session, user_id: int) -> Dict[str, Any]:
    # 1. Fetch user's configured monthly income
    income_record = db.query(Income).filter(Income.user_id == user_id).first()
    monthly_income = float(income_record.monthly_income) if income_record else 0.0
    has_salary_configured = income_record is not None and monthly_income > 0

    # 2. Query all expenses for user
    user_expenses = db.query(Expense).filter(Expense.user_id == user_id).all()

    total_lifetime_expenses = sum(float(e.amount) for e in user_expenses)
    total_transaction_count = len(user_expenses)
    average_expense = round(total_lifetime_expenses / total_transaction_count, 2) if total_transaction_count > 0 else 0.0
    highest_expense = max((float(e.amount) for e in user_expenses), default=0.0)

    # 3. Monthly expenses for current month
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    current_month_exp_list = [
        float(e.amount) for e in user_expenses
        if e.expense_date.year == current_year and e.expense_date.month == current_month
    ]
    current_month_expenses = sum(current_month_exp_list)

    # If current calendar month has zero expenses, fallback to total lifetime or latest month
    monthly_expenses = current_month_expenses
    if monthly_expenses == 0.0 and total_lifetime_expenses > 0:
        monthly_expenses = total_lifetime_expenses

    # 4. Monthly Savings & Savings Rate
    monthly_savings = monthly_income - monthly_expenses
    if monthly_income > 0:
        savings_rate = round((monthly_savings / monthly_income) * 100.0, 1)
    else:
        savings_rate = 0.0

    # 5. Annual Figures (Section 13 & 36)
    annual_income = monthly_income * 12.0
    annual_expenses = monthly_expenses * 12.0
    annual_savings = annual_income - annual_expenses

    # 6. Weekly Estimates (Annual / 52)
    estimated_weekly_income = round(annual_income / 52.0, 2)
    estimated_weekly_expenses = round(annual_expenses / 52.0, 2)
    estimated_weekly_savings = round(annual_savings / 52.0, 2)

    # 7. Category-wise expense distribution
    category_map = defaultdict(lambda: {"amount": 0.0, "count": 0})
    for e in user_expenses:
        cat = e.category or "Other"
        category_map[cat]["amount"] += float(e.amount)
        category_map[cat]["count"] += 1

    category_distribution: List[Dict[str, Any]] = []
    most_used_category = None
    max_count = 0

    for cat_name, stats in category_map.items():
        cat_amount = stats["amount"]
        count = stats["count"]
        pct = round((cat_amount / total_lifetime_expenses) * 100.0, 1) if total_lifetime_expenses > 0 else 0.0
        color = CATEGORY_COLORS.get(cat_name, "#2563EB")
        category_distribution.append({
            "category": cat_name,
            "amount": round(cat_amount, 2),
            "percentage": pct,
            "count": count,
            "color_hex": color
        })
        if count > max_count:
            max_count = count
            most_used_category = cat_name

    category_distribution.sort(key=lambda x: x["amount"], reverse=True)

    # 8. Monthly Spending Trend (Month-by-month aggregation)
    monthly_map = defaultdict(float)
    for e in user_expenses:
        m_str = e.expense_date.strftime("%Y-%m")
        monthly_map[m_str] += float(e.amount)

    monthly_trend: List[Dict[str, Any]] = []
    for m_str in sorted(monthly_map.keys()):
        exp_val = monthly_map[m_str]
        sav_val = monthly_income - exp_val
        monthly_trend.append({
            "month": m_str,
            "income": round(monthly_income, 2),
            "expenses": round(exp_val, 2),
            "savings": round(sav_val, 2)
        })

    # Ensure at least current month is represented
    if not monthly_trend:
        current_m_str = now.strftime("%Y-%m")
        monthly_trend.append({
            "month": current_m_str,
            "income": round(monthly_income, 2),
            "expenses": round(monthly_expenses, 2),
            "savings": round(monthly_savings, 2)
        })

    overview = {
        "monthly_income": round(monthly_income, 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "monthly_savings": round(monthly_savings, 2),
        "savings_rate": savings_rate,
        "annual_income": round(annual_income, 2),
        "annual_expenses": round(annual_expenses, 2),
        "annual_savings": round(annual_savings, 2),
        "estimated_weekly_income": estimated_weekly_income,
        "estimated_weekly_expenses": estimated_weekly_expenses,
        "estimated_weekly_savings": estimated_weekly_savings,
        "total_lifetime_expenses": round(total_lifetime_expenses, 2),
        "average_expense_amount": average_expense,
        "highest_expense_amount": round(highest_expense, 2),
        "most_used_category": most_used_category,
        "total_transaction_count": total_transaction_count
    }

    return {
        "overview": overview,
        "category_distribution": category_distribution,
        "monthly_trend": monthly_trend,
        "has_salary_configured": has_salary_configured
    }
