from typing import Optional, Dict
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    description: str = Field(..., min_length=1, description="Transaction description, e.g. Swiggy dinner")
    amount: float = Field(..., gt=0, description="Transaction amount in INR")
    merchant: Optional[str] = None
    payment_method: Optional[str] = "UPI"
    transaction_date: Optional[str] = None


class PredictionResponse(BaseModel):
    category: str
    confidence: float
    model_name: str
    probabilities: Optional[Dict[str, float]] = None
