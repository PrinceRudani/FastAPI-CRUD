from pydantic import BaseModel


class SubcategoryDTO(BaseModel):
    category_id: int
    subcategory_name: str
    subcategory_description: str

    class Config:
        from_attributes = True
