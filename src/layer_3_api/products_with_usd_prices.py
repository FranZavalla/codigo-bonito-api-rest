from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from layer_0_db_definition.database import get_database
from layer_1_repositories.product import ProductRepository
from layer_2_logic.connectors.bluelytics_connector import BluelyticsConnector
from layer_2_logic.product_with_dollar_blue import ProductWithDollarBluePrices


router = APIRouter()


@router.get("")
def get_products_with_usd_price(db: Session = Depends(get_database)):
    try:
        dollar_blue_repository = ProductWithDollarBluePrices(
            ProductRepository(db), BluelyticsConnector()
        )

        return dollar_blue_repository.get_products()
    except Exception as e:
        return {"error": str(e)}


@router.get("/{product_id}")
def get_product_with_usd_price(product_id: int, db: Session = Depends(get_database)):
    try:
        dollar_blue_repository = ProductWithDollarBluePrices(
            ProductRepository(db), BluelyticsConnector()
        )

        return dollar_blue_repository.get_product(product_id)
    except Exception as e:
        return {"error": str(e)}
