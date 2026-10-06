from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class User(Base):
    __tablename__ = "USERS"

    user_id = Column("USER_ID", Integer, primary_key=True, autoincrement=True)
    email = Column("EMAIL", String(120), unique=True, nullable=False, index=True)
    password_hash = Column("PASSWORD_HASH", String(255), nullable=False)
    full_name = Column("FULL_NAME", String(120), nullable=False)
    created_at = Column("CREATED_AT", DateTime, default=func.now())

    income = relationship("Income", back_populates="user", uselist=False, cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    prediction_logs = relationship("PredictionLog", back_populates="user")
