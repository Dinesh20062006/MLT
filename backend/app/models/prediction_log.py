from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class PredictionLog(Base):
    __tablename__ = "PREDICTION_LOGS"

    log_id = Column("LOG_ID", Integer, primary_key=True, autoincrement=True)
    user_id = Column("USER_ID", Integer, ForeignKey("USERS.USER_ID", ondelete="SET NULL"), nullable=True)
    input_description = Column("INPUT_DESCRIPTION", String(255), nullable=False)
    input_amount = Column("INPUT_AMOUNT", Float)
    predicted_category = Column("PREDICTED_CATEGORY", String(50), nullable=False)
    confidence = Column("CONFIDENCE", Float)
    model_name = Column("MODEL_NAME", String(100), nullable=False)
    created_at = Column("CREATED_AT", DateTime, default=func.now())

    user = relationship("User", back_populates="prediction_logs")
