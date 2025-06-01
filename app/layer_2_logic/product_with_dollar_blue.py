from typing import List

from app.layer_1_data_access.connectors.dollar_connector import DollarConnector
from app.layer_1_data_access.repositories.product_abstract import (
    AbstractProductRepository,
    ProductData,
)


class ProductDataWithUSDPrice(ProductData):
    usd_price: float


class ProductWithDollarBluePrices:
    def __init__(
        self,
        product_repository: AbstractProductRepository,
        dollar_blue_connector: DollarConnector,
    ):
        self.product_repository = product_repository
        self.dollar_blue_connector = dollar_blue_connector

    def get_product(self, product_id: int) -> ProductDataWithUSDPrice:
        """
        Retrieves a product by its ID and calculates its price in USD using the dollar blue exchange rate.

        Parameters:
            product_id (int): The ID of the product to retrieve.

        Returns:
            ProductDataWithUSDPrice: An object containing the product details along with its price in USD.

        Raises:
            ValueError: If the product is not found or if there is an error fetching the dollar blue price.
        """
        try:
            product = self.product_repository.get_by_id(product_id)
        except ValueError as e:
            raise e

        try:
            dollar_blue_price = self.dollar_blue_connector.get_price()
        except ValueError as e:
            raise Exception("Error getting dollar blue price")

        return ProductDataWithUSDPrice(
            id=product.id,
            name=product.name,
            price=product.price,
            usd_price=round(product.price / dollar_blue_price, 2),
        )

    def get_products(self) -> List[ProductDataWithUSDPrice]:
        """
        Retrieves a list of products with their prices converted to USD using the dollar blue exchange rate.

        Returns:
            List[ProductDataWithUSDPrice]: A list of products, each containing the product ID, name,
            original price, and price converted to USD.

        Raises:
            ValueError: If there is an issue retrieving the dollar blue exchange rate.
        """
        products = self.product_repository.get_all()

        try:
            dollar_blue_price = self.dollar_blue_connector.get_price()
        except ValueError as e:
            raise e

        return [
            ProductDataWithUSDPrice(
                id=product.id,
                name=product.name,
                price=product.price,
                usd_price=round(product.price / dollar_blue_price, 2),
            )
            for product in products
        ]
