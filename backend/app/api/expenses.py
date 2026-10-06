from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.expense import Expense
from backend.app.schemas.expense import (
    ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseListResponse
)
from backend.app.utils.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_in: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if expense_in.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    expense_date = expense_in.expense_date or date.today()

    expense = Expense(
        user_id=current_user.user_id,
        description=expense_in.description.strip(),
        amount=expense_in.amount,
        category=expense_in.category.strip(),
        predicted_category=expense_in.predicted_category,
        merchant=expense_in.merchant.strip() if expense_in.merchant else None,
        payment_method=expense_in.payment_method or "UPI",
        expense_date=expense_date
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=ExpenseListResponse)
def list_expenses(
    search: Optional[str] = Query(None, description="Search description or merchant"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[date] = Query(None, description="Filter from date"),
    end_date: Optional[date] = Query(None, description="Filter to date"),
    sort_by: Optional[str] = Query("expense_date", pattern="^(expense_date|amount|description|category)$"),
    sort_order: Optional[str] = Query("desc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Expense).filter(Expense.user_id == current_user.user_id)

    # Search filter
    if search and search.strip():
        term = f"%{search.strip().lower()}%"
        query = query.filter(
            (Expense.description.ilike(term)) | (Expense.merchant.ilike(term))
        )

    # Category filter
    if category and category.strip() and category != "All":
        query = query.filter(Expense.category == category.strip())

    # Date range filters
    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)

    total = query.count()

    # Sort
    col = getattr(Expense, sort_by, Expense.expense_date)
    order_func = desc if sort_order == "desc" else asc
    query = query.order_by(order_func(col))

    # Pagination
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    total_pages = max(1, (total + page_size - 1) // page_size)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "expenses": items
    }


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.expense_id == expense_id,
        Expense.user_id == current_user.user_id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_in: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.expense_id == expense_id,
        Expense.user_id == current_user.user_id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense_in.description is not None:
        expense.description = expense_in.description.strip()
    if expense_in.amount is not None:
        if expense_in.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        expense.amount = expense_in.amount
    if expense_in.category is not None:
        expense.category = expense_in.category.strip()
    if expense_in.predicted_category is not None:
        expense.predicted_category = expense_in.predicted_category
    if expense_in.merchant is not None:
        expense.merchant = expense_in.merchant.strip()
    if expense_in.payment_method is not None:
        expense.payment_method = expense_in.payment_method
    if expense_in.expense_date is not None:
        expense.expense_date = expense_in.expense_date

    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_200_OK)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.expense_id == expense_id,
        Expense.user_id == current_user.user_id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully", "expense_id": expense_id}
