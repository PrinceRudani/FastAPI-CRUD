from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubcategoryDTO(BaseModel):
    subcategory_category_id: int
    subcategory_name: str
    subcategory_description: Optional[str] = None  # Optional field

    model_config = ConfigDict(from_attributes=True)  # Enables ORM conversion


class UpdateSubcategoryDTO(BaseModel):
    id: int
    subcategory_category_id: int

    subcategory_name: str
    subcategory_description: str

    class Config:
        from_attributes = True
