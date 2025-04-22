from typing import List

from pony.orm import commit, db_session, select

from layer_0_db_definition.models_ponyorm import Product
from layer_0_db_definition.schema import ProductCreate

from .product_abstract import AbstractProductRepository


class ProductRepository(AbstractProductRepository):
    @db_session
    def get_all(self) -> List[Product]:
        return [p.to_dict() for p in select(p for p in Product)]

    @db_session
    def get_by_id(self, product_id: int) -> Product:
        product = Product.get(id=product_id)
        if not product:
            raise ValueError("Product does not exist")
        return product.to_dict()

    @db_session
    def create(self, product: ProductCreate) -> Product:
        product_data = product.model_dump()
        new_product = Product(**product_data)
        return new_product

    @db_session
    def update_with_factor(self, factor: float) -> None:
        for p in Product.select():
            p.price *= factor
        commit()
