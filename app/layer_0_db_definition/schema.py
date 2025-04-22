from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float


class ProductRead(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True


class ProductReadWithUSDPrice(ProductRead):
    usd_price: float
