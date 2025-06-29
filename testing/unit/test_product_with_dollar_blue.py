from typing import Tuple

import pytest

from app.layer_1_data_access.repositories.product_abstract import \
    AbstractProductRepository
from app.layer_2_logic.product_with_dollar_blue import (
    DollarConnector, ProductWithDollarBluePrices)
from testing.mocks.layer_one_mocks import (
    get_mock_dollar_connector_with_exception,
    get_mock_dollar_connector_with_happy_response,
    get_mock_product_respository_happy_response)


@pytest.fixture
def init_classes() -> Tuple[AbstractProductRepository, DollarConnector]:
    return [
        get_mock_product_respository_happy_response(),
        get_mock_dollar_connector_with_happy_response(),
    ]


@pytest.fixture
def init_classes_with_exception() -> Tuple[AbstractProductRepository, DollarConnector]:
    return [
        get_mock_product_respository_happy_response(),
        get_mock_dollar_connector_with_exception(),
    ]


def test_product_with_dollar_blue(init_classes):
    product_repository, dollar_connector = init_classes
    product_with_dollar_blue = ProductWithDollarBluePrices(
        product_repository, dollar_connector
    )

    original_product = product_repository.get_by_id(1)
    dollar_price = dollar_connector.get_price()
    product = product_with_dollar_blue.get_product(1)

    assert product.id == original_product.id
    assert product.name == original_product.name
    assert product.price == original_product.price
    assert product.usd_price == round(original_product.price / dollar_price, 2)


def test_non_existing_product(init_classes):
    product_repository, dollar_connector = init_classes
    product_with_dollar_blue = ProductWithDollarBluePrices(
        product_repository, dollar_connector
    )
    with pytest.raises(ValueError):
        product_with_dollar_blue.get_product(4)


def test_product_with_exception(init_classes_with_exception):
    product_repository, dollar_connector = init_classes_with_exception
    product_with_dollar_blue = ProductWithDollarBluePrices(
        product_repository, dollar_connector
    )
    with pytest.raises(Exception):
        product_with_dollar_blue.get_product(1)


def test_products_with_dollar_blue_prices(init_classes):
    product_repository, dollar_connector = init_classes
    product_with_dollar_blue = ProductWithDollarBluePrices(
        product_repository, dollar_connector
    )

    original_products = product_repository.get_all()
    products = product_with_dollar_blue.get_products()
    dollar_price = dollar_connector.get_price()

    assert len(original_products) == len(products)
    for original_product, product in zip(original_products, products):
        assert product.id == original_product.id
        assert product.name == original_product.name
        assert product.price == original_product.price
        assert product.usd_price == round(original_product.price / dollar_price, 2)


def test_products_with_exception(init_classes_with_exception):
    product_repository, dollar_connector = init_classes_with_exception
    product_with_dollar_blue = ProductWithDollarBluePrices(
        product_repository, dollar_connector
    )
    with pytest.raises(ValueError):
        product_with_dollar_blue.get_products()
