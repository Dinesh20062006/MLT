from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.app.database.session import Base


class Category(Base):
    __tablename__ = "CATEGORIES"

    category_id = Column("CATEGORY_ID", Integer, primary_key=True, autoincrement=True)
    name = Column("NAME", String(50), unique=True, nullable=False)
    description = Column("DESCRIPTION", String(255))
    color_hex = Column("COLOR_HEX", String(10), default="#2563EB")
    icon_name = Column("ICON_NAME", String(50), default="Tag")
    created_at = Column("CREATED_AT", DateTime, default=func.now())
