from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.layer_0_db_definition.database_sqlalchemy import get_database
from app.layer_1_data_access.connectors.bluelytics_connector import BluelyticsConnector
from app.layer_1_data_access.repositories.Product.utils import get_product_repository
from app.layer_2_logic.product_with_dollar_blue import ProductWithDollarBluePrices

router = APIRouter()


@router.get("")
def get_products_with_usd_price(db: Session = Depends(get_database)):
    try:
        dollar_blue_repository = ProductWithDollarBluePrices(
            get_product_repository(db), BluelyticsConnector()
        )

        return dollar_blue_repository.get_products()
    except Exception as e:
        return {"error": str(e)}


@router.get("/{product_id}")
def get_product_with_usd_price(product_id: int, db: Session = Depends(get_database)):
    try:
        dollar_blue_repository = ProductWithDollarBluePrices(
            get_product_repository(db), BluelyticsConnector()
        )

        return dollar_blue_repository.get_product(product_id)
    except Exception as e:
        return {"error": str(e)}
