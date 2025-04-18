from layer_0_db_definition.models import Product
from layer_0_db_definition.schema import ProductCreate
from sqlalchemy.orm import Session
from typing import List


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]:
        """
        Retrieve all Product rows from the database.

        Returns:
          List[Product]: A list of all Product objects stored in the database.
        """
        return self.db.query(Product).all()

    def get_by_id(self, product_id: int) -> Product:
        """
        Retrieve a product by its unique identifier.

        Args:
          product_id (int): The unique identifier of the product to retrieve.

        Returns:
          Product: The product instance corresponding to the given ID.

        Raises:
          ValueError: If no product with the given ID exists in the database.
        """
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product does not exist")
        return product

    def create(self, product: ProductCreate) -> Product:
        """
        Create a new product in the database.

        Parameters:
          product (Product): The product instance to be created.

        Returns:
          Product: The created product instance.
        """
        product_parsed = Product(**product.model_dump())
        self.db.add(product_parsed)
        self.db.commit()
        self.db.refresh(product_parsed)
        return product_parsed

    def update_with_factor(self, factor: float) -> None:
        """
        Update the price of all products in the database by a given factor.

        Parameters:
          factor (float): The factor by which to multiply the price of each product.
        """
        self.db.query(Product).update({Product.price: Product.price * factor})
        self.db.commit()
