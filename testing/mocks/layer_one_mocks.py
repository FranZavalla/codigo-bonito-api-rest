from unittest.mock import MagicMock

from app.layer_1_data_access.repositories.Product.product_abstract import \
    ProductData


def get_mock_product_respository_happy_response():
    products = [
        ProductData(id=1, name="Pretty shirt", price=7500.0),
        ProductData(id=2, name="Cool mug", price=4000.0),
        ProductData(id=3, name="TV 4K", price=1500000.0),
    ]

    mock_response = MagicMock()
    mock_response.get_all.return_value = products

    def get_by_id(product_id: int) -> ProductData:
        for product in products:
            if product.id == product_id:
                return product
        raise ValueError(f"Product with id {product_id} not found")

    mock_response.get_by_id = get_by_id

    return mock_response


def get_mock_dollar_connector_with_happy_response():
    mock_response = MagicMock()
    mock_response.get_price.return_value = 1
    return mock_response


def get_mock_dollar_connector_with_exception():
    mock_response = MagicMock()
    mock_response.get_price.side_effect = ValueError("Error getting price")
    return mock_response
