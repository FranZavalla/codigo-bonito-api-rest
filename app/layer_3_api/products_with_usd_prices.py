from fastapi import APIRouter, Depends

from app.layer_1_data_access.connectors.bluelytics_connector import BluelyticsConnector
from app.layer_1_data_access.repositories.Product.product_abstract import (
    AbstractProductRepository,
)
from app.layer_2_logic.product_with_dollar_blue import ProductWithDollarBluePrices
from app.layer_3_api.utils import get_product_repository

router = APIRouter()


@router.get("")
def get_products_with_usd_price(
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        dollar_blue_repository = ProductWithDollarBluePrices(
            product_repository, BluelyticsConnector()
        )

        return dollar_blue_repository.get_products()
    except Exception as e:
        return {"error": str(e)}


@router.get("/{product_id}")
def get_product_with_usd_price(
    product_id: int,
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        dollar_blue_repository = ProductWithDollarBluePrices(
            product_repository, BluelyticsConnector()
        )

        return dollar_blue_repository.get_product(product_id)
    except Exception as e:
        return {"error": str(e)}
