from typing import List

from pony.orm import commit, db_session, select

from app.layer_0_db_definition.models_ponyorm import Product

from app.layer_1_data_access.repositories.Product.product_abstract import (
    AbstractProductRepository,
    ProductData,
    CreateProductData,
)


class PonyProductRepository(AbstractProductRepository):
    @db_session
    def get_all(self) -> List[ProductData]:
        products = select(p for p in Product)
        return [ProductData.model_validate(p.to_dict()) for p in products]

    @db_session
    def get_by_id(self, product_id: int) -> ProductData:
        product = Product.get(id=product_id)
        if not product:
            raise ValueError("Product does not exist")
        return ProductData.model_validate(product.to_dict())

    @db_session
    def create(self, product: CreateProductData) -> ProductData:
        product_data = product.model_dump()
        new_product = Product(**product_data)
        return ProductData.model_validate(new_product.to_dict())

    @db_session
    def update_with_factor(self, factor: float) -> None:
        for p in Product.select():
            p.price *= factor
        commit()
