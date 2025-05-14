from pydantic import BaseModel


class ProductData(BaseModel):
    id: int
    name: str
    price: float

    model_config = {"from_attributes": True}


class CreateProductData(BaseModel):
    name: str
    price: float
