from fastapi import Form
from pydantic import BaseModel


class CategoryDTO(BaseModel):
    category_name: str
    category_description: str


class UpdateCategoryDTO(BaseModel):
    id: int
    category_name: str
    category_description: str

class CategoryResponse(CategoryDTO):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True
