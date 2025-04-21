from layer_1_repositories.product_sqlachemy import ProductRepository
# from layer_1_repositories.product_pony import ProductRepository
from layer_0_db_definition.schema import ProductReadWithUSDPrice
from .connectors.bluelytics_connector import BluelyticsConnector
from typing import List


class ProductWithDollarBluePrices:
    def __init__(
        self,
        product_repository: ProductRepository,
        dollar_blue_connector: BluelyticsConnector,
    ):
        self.product_repository = product_repository
        self.dollar_blue_connector = dollar_blue_connector

    def get_product(self, product_id: int) -> ProductReadWithUSDPrice:
        """
        Retrieves a product by its ID and calculates its price in USD using the dollar blue exchange rate.

        Parameters:
            product_id (int): The ID of the product to retrieve.

        Returns:
            ProductReadWithUSDPrice: An object containing the product details along with its price in USD.

        Raises:
            ValueError: If the product is not found or if there is an error fetching the dollar blue price.
        """
        try:
            product = self.product_repository.get_by_id(product_id)
            dollar_blue_price = self.dollar_blue_connector.get_price()
        except ValueError as e:
            raise e

        return ProductReadWithUSDPrice(
            id=product.id,
            name=product.name,
            price=product.price,
            usd_price=round(product.price / dollar_blue_price, 2),
        )

    def get_products(self) -> List[ProductReadWithUSDPrice]:
        """
        Retrieves a list of products with their prices converted to USD using the dollar blue exchange rate.

        Returns:
            List[ProductReadWithUSDPrice]: A list of products, each containing the product ID, name,
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
            ProductReadWithUSDPrice(
                id=product.id,
                name=product.name,
                price=product.price,
                usd_price=round(product.price / dollar_blue_price, 2),
            )
            for product in products
        ]
