from typing import List
from app.layer_1_data_access.repositories.Product.product_abstract import (
    AbstractProductRepository,
    ProductData,
    CreateProductData,
)
from app.layer_2_logic.product_with_dollar_blue import (
    DollarConnector,
)


class MockProductRepository(AbstractProductRepository):
    def __init__(self):
        self.products = [
            ProductData(id=1, name="Pretty shirt", price=7500.0),
            ProductData(id=2, name="Cool mug", price=4000.0),
            ProductData(id=3, name="TV 4K", price=1500000.0),
        ]

    def get_all(self) -> List[ProductData]:
        return self.products

    def get_by_id(self, product_id: int) -> ProductData:
        for product in self.products:
            if product.id == product_id:
                return product
        raise ValueError("Product not found")

    def create(self, product: CreateProductData) -> ProductData:
        self.products.append(product)
        return product

    def update_with_factor(self, factor: float) -> None:
        for product in self.products:
            product.price *= factor


class MockDollarConnector(DollarConnector):
    def __init__(self):
        self.price = 1

    def get_price(self) -> float:
        return self.price
