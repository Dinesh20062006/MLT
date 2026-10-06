from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class Expense(Base):
    __tablename__ = "EXPENSES"

    expense_id = Column("EXPENSE_ID", Integer, primary_key=True, autoincrement=True)
    user_id = Column("USER_ID", Integer, ForeignKey("USERS.USER_ID", ondelete="CASCADE"), nullable=False)
    description = Column("DESCRIPTION", String(255), nullable=False)
    amount = Column("AMOUNT", Float, nullable=False)
    category = Column("CATEGORY", String(50), nullable=False, index=True)
    predicted_category = Column("PREDICTED_CATEGORY", String(50))
    merchant = Column("MERCHANT", String(100))
    payment_method = Column("PAYMENT_METHOD", String(50), default="UPI")
    expense_date = Column("EXPENSE_DATE", Date, nullable=False)
    created_at = Column("CREATED_AT", DateTime, default=func.now())

    user = relationship("User", back_populates="expenses")
