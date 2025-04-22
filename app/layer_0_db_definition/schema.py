from pydantic import BaseModel


class ProductRequestData(BaseModel):
    name: str
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True


class ProductResponseWithUSDPrice(ProductResponse):
    usd_price: float
