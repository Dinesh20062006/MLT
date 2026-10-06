from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IncomeCreateOrUpdate(BaseModel):
    monthly_income: float = Field(..., ge=0, description="Monthly income in INR")


class IncomeResponse(BaseModel):
    income_id: int
    user_id: int
    monthly_income: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
