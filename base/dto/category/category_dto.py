from fastapi import Form
from pydantic import BaseModel


class CategoryDTO(BaseModel):
    category_name: str
    category_description: str

    @classmethod
    def as_form(
        cls, category_name: str = Form(...), category_description: str = Form(...)
    ):
        return cls(
            category_name=category_name, category_description=category_description
        )


class CategoryResponse(CategoryDTO):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True
