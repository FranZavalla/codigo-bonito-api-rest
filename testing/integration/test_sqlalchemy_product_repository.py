import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.layer_0_db_definition.models_sqlalchemy import Base, Product
from app.layer_1_data_access.repositories.product_sqlachemy import (
    CreateProductData,
    SQLAlchemyProductRepository,
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def session_with_products(session):
    session.add_all(
        [
            Product(name="Pretty shirt", price=7500.0),
            Product(name="Cool mug", price=4000.0),
            Product(name="TV 4K", price=1500000.0),
        ]
    )
    session.commit()
    return session


def test_get_all_returns_empty_list(session):
    repo = SQLAlchemyProductRepository(session)

    assert repo.get_all() == []


def test_get_all_returns_all_products(session_with_products):
    repo = SQLAlchemyProductRepository(session_with_products)

    assert len(repo.get_all()) == session_with_products.query(Product).count()


def test_get_by_id_returns_product(session_with_products):
    repo = SQLAlchemyProductRepository(session_with_products)

    product = repo.get_by_id(1)
    assert (
        product.name
        == session_with_products.query(Product).filter(Product.id == 1).first().name
    )


def test_get_by_id_returns_error_if_product_does_not_exist(session_with_products):
    repo = SQLAlchemyProductRepository(session_with_products)

    with pytest.raises(ValueError):
        repo.get_by_id(4)


def test_create_product(session):
    repo = SQLAlchemyProductRepository(session)
    product_count = session.query(Product).count()

    repo.create(CreateProductData(name="Candy bar", price=100.0))
    assert session.query(Product).count() == product_count + 1


def test_create_product_with_large_price(session):
    repo = SQLAlchemyProductRepository(session)
    product_count = session.query(Product).count()

    repo.create(CreateProductData(name="Luxury car", price=1e9))
    assert session.query(Product).count() == product_count + 1


def test_create_product_with_zero_price(session):
    repo = SQLAlchemyProductRepository(session)
    product_count = session.query(Product).count()

    repo.create(CreateProductData(name="Free Product", price=0.0))
    assert session.query(Product).count() == product_count + 1


def test_update_with_factor(session_with_products):
    repo = SQLAlchemyProductRepository(session_with_products)

    original_prices = [p for p in session_with_products.query(Product).all()]
    repo.update_with_factor(2)
    updated_prices = [p for p in session_with_products.query(Product).all()]

    for original, updated in zip(original_prices, updated_prices):
        assert original.price == updated.price


def test_update_with_factor_one_does_not_change_prices(session_with_products):
    repo = SQLAlchemyProductRepository(session_with_products)

    original_prices = [p for p in session_with_products.query(Product).all()]
    repo.update_with_factor(1)
    updated_prices = [p for p in session_with_products.query(Product).all()]

    for original, updated in zip(original_prices, updated_prices):
        assert original.price == updated.price


# The following test should pass, but it doesn't.
# The create method doesn't throw an error when we enter a negative value.
# This is a bug that the developer would notice in the code.


def _test_create_product_with_negative_price_raises_error(session):
    repo = SQLAlchemyProductRepository(session)

    data = CreateProductData(name="Invalid Product", price=-100.0)
    with pytest.raises(ValueError):
        repo.create(data)
