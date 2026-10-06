from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class Income(Base):
    __tablename__ = "INCOME"

    income_id = Column("INCOME_ID", Integer, primary_key=True, autoincrement=True)
    user_id = Column("USER_ID", Integer, ForeignKey("USERS.USER_ID", ondelete="CASCADE"), nullable=False, unique=True)
    monthly_income = Column("MONTHLY_INCOME", Float, default=0.0, nullable=False)
    created_at = Column("CREATED_AT", DateTime, default=func.now())
    updated_at = Column("UPDATED_AT", DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="income")
