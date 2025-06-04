import os
import requests

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.layer_0_db_definition.models_sqlalchemy import Product


@pytest.fixture(autouse=True)
def clear_db():
    database_path = os.getenv("DATABASE_PATH", "./test_db.sqlite")
    database_url = f"sqlite:///{database_path}"

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.query(Product).delete()
        session.commit()

        products = [
            Product(name="Pretty shirt", price=7500.0),
            Product(name="Cool mug", price=4000.0),
            Product(name="TV 4K", price=1500000.0),
        ]
        session.add_all(products)
        session.commit()
    finally:
        session.close()

    yield

    session = Session()
    try:
        session.query(Product).delete()
        session.commit()
    finally:
        session.close()


def test_health_check():
    response = requests.get("http://localhost:8000/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Healthy"}


def test_get_products_returns_200(clear_db):
    response = requests.get("http://localhost:8000/products")
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json()["detail"], list)
    assert len(response.json()["detail"]) == 3


def test_create_product_returns_201(clear_db):
    response = requests.post(
        "http://localhost:8000/products", json={"name": "Luxury car", "price": 1e9}
    )
    assert response.status_code == 201
    assert response.json() == {"detail": "Product created"}


def test_create_product_returns_422_if_the_product_is_invalid(clear_db):
    response = requests.post(
        "http://localhost:8000/products", json={"name": "Luxury car"}
    )
    assert response.status_code == 422


def test_get_product_returns_200(clear_db):
    response = requests.get("http://localhost:8000/products/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Pretty shirt", "price": 7500.0}


def test_get_product_returns_422_if_the_product_id_is_not_a_number(clear_db):
    response = requests.get("http://localhost:8000/products/NOTANUMBER")
    assert response.status_code == 422


def test_get_product_returns_404_if_the_product_does_not_exist(clear_db):
    response = requests.get("http://localhost:8000/products/4")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_update_products_price_returns_200(clear_db):
    response = requests.put("http://localhost:8000/products?factor=1.1")
    assert response.status_code == 200


def test_update_products_price_returns_422_if_the_factor_is_invalid(clear_db):
    response = requests.put("http://localhost:8000/products?factor=NOTANUMBER")
    assert response.status_code == 422


def test_get_products_with_usd_prices_returns_200(clear_db):
    response = requests.get("http://localhost:8000/products_with_usd_prices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


def test_get_product_with_usd_prices_returns_200(clear_db):
    response = requests.get("http://localhost:8000/products_with_usd_prices/1")
    assert response.status_code == 200


def test_get_product_with_usd_prices_returns_422_if_the_product_id_is_not_a_number(
    clear_db,
):
    response = requests.get("http://localhost:8000/products_with_usd_prices/NOTANUMBER")
    assert response.status_code == 422


def test_get_product_with_usd_prices_returns_404_if_the_product_does_not_exist(
    clear_db,
):
    response = requests.get("http://localhost:8000/products_with_usd_prices/4")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
