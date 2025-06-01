from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class ProductData(BaseModel):
    id: int
    name: str
    price: float

    model_config = {"from_attributes": True}


class CreateProductData(BaseModel):
    name: str
    price: float


class AbstractProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[ProductData]:
        """
        Retrieve all Product rows from the database.

        Returns:
          List[Product]: A list of all Product objects stored in the database.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> ProductData:
        """
        Retrieve a product by its unique identifier.

        Args:
          product_id (int): The unique identifier of the product to retrieve.

        Returns:
          Product: The product instance corresponding to the given ID.

        Raises:
          ValueError: If no product with the given ID exists in the database.
        """
        pass

    @abstractmethod
    def create(self, product: CreateProductData) -> ProductData:
        """
        Create a new product in the database.

        Parameters:
          product (Product): The product instance to be created.

        Returns:
          Product: The created product instance.
        """
        pass

    @abstractmethod
    def update_with_factor(self, factor: float) -> None:
        """
        Update the price of all products in the database by a given factor.

        Parameters:
          factor (float): The factor by which to multiply the price of each product.
        """
        pass
