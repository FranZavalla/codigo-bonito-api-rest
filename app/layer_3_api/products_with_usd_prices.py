from fastapi import APIRouter, Depends

from app.layer_2_logic.product_with_dollar_blue import ProductWithDollarBluePrices
from app.layer_2_logic.utils import get_dollar_blue_repository

router = APIRouter()


@router.get("")
def get_products_with_usd_price(
    dollar_blue_repository: ProductWithDollarBluePrices = Depends(
        get_dollar_blue_repository
    ),
):
    try:
        return dollar_blue_repository.get_products()
    except Exception as e:
        return {"error": str(e)}


@router.get("/{product_id}")
def get_product_with_usd_price(
    product_id: int,
    dollar_blue_repository: ProductWithDollarBluePrices = Depends(
        get_dollar_blue_repository
    ),
):
    try:
        return dollar_blue_repository.get_product(product_id)
    except Exception as e:
        return {"error": str(e)}
