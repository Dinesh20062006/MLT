from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0, description="Expense amount must be positive")
    category: str = Field(..., min_length=1, max_length=50)
    predicted_category: Optional[str] = None
    merchant: Optional[str] = None
    payment_method: Optional[str] = "UPI"
    expense_date: Optional[date] = None


class ExpenseUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    predicted_category: Optional[str] = None
    merchant: Optional[str] = None
    payment_method: Optional[str] = None
    expense_date: Optional[date] = None


class ExpenseResponse(BaseModel):
    expense_id: int
    user_id: int
    description: str
    amount: float
    category: str
    predicted_category: Optional[str] = None
    merchant: Optional[str] = None
    payment_method: Optional[str] = None
    expense_date: date
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExpenseListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    expenses: List[ExpenseResponse]
