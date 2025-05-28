import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.layer_0_db_definition.models_sqlalchemy import Base, Product
from app.main import app
from app.settings import DATABASE_URL, settings

client = TestClient(app)


@pytest.fixture(scope="function")
def init_db():
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), settings.DATABASE_PATH
    )
    if os.path.exists(path):
        os.remove(path)

    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    db.query(Product).delete()
    db.commit()

    db.add(Product(name="Pretty shirt", price=7500.0))
    db.add(Product(name="Cool mug", price=4000.0))
    db.add(Product(name="TV 4K", price=1500000.0))
    db.commit()

    yield db

    db.close()


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Healthy"}


def test_get_products_returns_200(init_db):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


def test_create_product_returns_201(init_db):
    response = client.post("/products", json={"name": "Luxury car", "price": 1e9})
    assert response.status_code == 201
    assert response.json() == "Product created"


def test_create_product_returns_422_if_the_product_is_invalid(init_db):
    response = client.post("/products", json={"name": "Luxury car"})
    assert response.status_code == 422


def test_get_product_returns_200(init_db):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Pretty shirt", "price": 7500.0}


def test_get_product_returns_422_if_the_product_id_is_not_a_number(init_db):
    response = client.get("/products/NOTANUMBER")
    assert response.status_code == 422


def test_get_product_returns_404_if_the_product_does_not_exist(init_db):
    response = client.get("/products/4")
    assert response.status_code == 404
    assert response.json() == "Product not found"


def test_update_products_price_returns_204(init_db):
    response = client.put("/products?factor=1.1")
    assert response.status_code == 204
    assert response.json() == "Prices updated"


def test_update_products_price_returns_422_if_the_factor_is_invalid(init_db):
    response = client.put("/products?factor=NOTANUMBER")
    assert response.status_code == 422


def test_get_products_with_usd_prices_returns_200(init_db):
    response = client.get("/products_with_usd_prices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


def test_get_product_with_usd_prices_returns_200(init_db):
    response = client.get("/products_with_usd_prices/1")
    assert response.status_code == 200


def test_get_product_with_usd_prices_returns_422_if_the_product_id_is_not_a_number(
    init_db,
):
    response = client.get("/products_with_usd_prices/NOTANUMBER")
    assert response.status_code == 422


def test_get_product_with_usd_prices_returns_404_if_the_product_does_not_exist(init_db):
    response = client.get("/products_with_usd_prices/4")
    assert response.status_code == 404
    assert response.json() == "Product not found"
