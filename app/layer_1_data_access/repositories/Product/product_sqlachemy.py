from typing import List

from sqlalchemy.orm import Session

from app.layer_0_db_definition.models_sqlalchemy import Product
from app.layer_0_db_definition.schema import CreateProductData, ProductData

from app.layer_1_data_access.repositories.Product.product_abstract import (
    AbstractProductRepository,
)


class SQLAlchemyProductRepository(AbstractProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ProductData]:
        products = self.db.query(Product).all()
        return [ProductData.model_validate(p) for p in products]

    def get_by_id(self, product_id: int) -> Product:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product does not exist")
        return ProductData.model_validate(product)

    def create(self, product: CreateProductData) -> Product:
        product_parsed = Product(**product.model_dump())
        self.db.add(product_parsed)
        self.db.commit()
        self.db.refresh(product_parsed)
        return ProductData.model_validate(product_parsed)

    def update_with_factor(self, factor: float) -> None:
        self.db.query(Product).update({Product.price: Product.price * factor})
        self.db.commit()
