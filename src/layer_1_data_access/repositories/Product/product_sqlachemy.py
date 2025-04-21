from typing import List

from sqlalchemy.orm import Session

from layer_0_db_definition.models_sqlalchemy import Product
from layer_0_db_definition.schema import ProductCreate

from .product_abstract import AbstractProductRepository


class ProductRepository(AbstractProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()

    def get_by_id(self, product_id: int) -> Product:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product does not exist")
        return product

    def create(self, product: ProductCreate) -> Product:
        product_parsed = Product(**product.model_dump())
        self.db.add(product_parsed)
        self.db.commit()
        self.db.refresh(product_parsed)
        return product_parsed

    def update_with_factor(self, factor: float) -> None:
        self.db.query(Product).update({Product.price: Product.price * factor})
        self.db.commit()
