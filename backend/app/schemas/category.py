from typing import Optional
from pydantic import BaseModel


class CategoryResponse(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    color_hex: Optional[str] = "#2563EB"
    icon_name: Optional[str] = "Tag"

    class Config:
        from_attributes = True
