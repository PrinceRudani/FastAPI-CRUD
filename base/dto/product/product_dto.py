from pydantic import BaseModel, Field
from typing import Optional


class ProductDTO(BaseModel):
    product_category_id: int = Field(...)
    product_subcategory_id: int = Field(...)
    product_name: str = Field(...)
    product_description: str = Field(...)
    product_price: int = Field(...)
    product_quantity: int = Field(...)


class UpdateProductDTO(ProductDTO):
    id: int
    product_image_name: Optional[str]
    product_image_path: Optional[str]

    class Config:
        from_attributes = True
