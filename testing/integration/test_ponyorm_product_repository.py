import pytest
from pony.orm import commit, db_session, count, select

from app.layer_0_db_definition.models_ponyorm import Product, db
from app.layer_1_data_access.repositories.product_pony import (
    CreateProductData,
    PonyProductRepository,
)


@pytest.fixture()
def fresh_db():
    db.bind(provider="sqlite", filename=":memory:", create_db=True)
    db.generate_mapping(create_tables=True)

    yield

    db.provider = None
    db.schema = None
    db.disconnect()


@pytest.fixture()
def db_with_products():
    db.bind(provider="sqlite", filename=":memory:", create_db=True)
    db.generate_mapping(create_tables=True)

    with db_session:
        Product(name="Pretty shirt", price=7500.0)
        Product(name="Cool mug", price=4000.0)
        Product(name="TV 4K", price=1500000.0)
        commit()

    yield

    db.provider = None
    db.schema = None
    db.disconnect()


def test_get_all_returns_empty_list(fresh_db):
    with db_session:
        repo = PonyProductRepository()

        assert repo.get_all() == []


def test_get_all_returns_all_products(db_with_products):
    with db_session:
        repo = PonyProductRepository()

        assert len(repo.get_all()) == count(p for p in Product)


def test_get_by_id_returns_product(db_with_products):
    with db_session:
        repo = PonyProductRepository()

        product = repo.get_by_id(1)
        assert product.name == Product.get(id=1).name


def test_get_by_id_returns_error_if_product_does_not_exist(db_with_products):
    with db_session:
        repo = PonyProductRepository()

        with pytest.raises(ValueError):
            repo.get_by_id(4)


def test_create_product(db_with_products):
    with db_session:
        repo = PonyProductRepository()
        product_count = count(p for p in Product)

        repo.create(CreateProductData(name="Candy bar", price=100.0))
        assert count(p for p in Product) == product_count + 1


def test_create_product_with_large_price(db_with_products):
    with db_session:
        repo = PonyProductRepository()
        product_count = count(p for p in Product)

        repo.create(CreateProductData(name="Luxury car", price=1e9))
        assert count(p for p in Product) == product_count + 1


def test_create_product_with_zero_price(db_with_products):
    with db_session:
        repo = PonyProductRepository()
        product_count = count(p for p in Product)

        repo.create(CreateProductData(name="Free Product", price=0.0))
        assert count(p for p in Product) == product_count + 1


def test_update_with_factor(db_with_products):
    with db_session:
        repo = PonyProductRepository()

        original_prices = select(p for p in Product)
        repo.update_with_factor(2)
        updated_prices = select(p for p in Product)

        for original, updated in zip(original_prices, updated_prices):
            assert original.price == updated.price


def test_update_with_factor_one_does_not_change_prices(db_with_products):
    with db_session:
        repo = PonyProductRepository()

        original_prices = select(p for p in Product)
        repo.update_with_factor(1)
        updated_prices = select(p for p in Product)

        for original, updated in zip(original_prices, updated_prices):
            assert original.price == updated.price
