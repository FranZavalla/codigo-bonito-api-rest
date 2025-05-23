from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.layer_2_logic.product_with_dollar_blue import ProductWithDollarBluePrices
from app.layer_2_logic.repository_factories import get_dollar_blue_repository

router = APIRouter()


@router.get("")
def get_products_with_usd_price(
    dollar_blue_repository: ProductWithDollarBluePrices = Depends(
        get_dollar_blue_repository
    ),
):
    try:
        products = dollar_blue_repository.get_products()
        return JSONResponse(status_code=200, content=products)
    except Exception:
        return JSONResponse(status_code=500, content="Internal server error")


@router.get("/{product_id}")
def get_product_with_usd_price(
    product_id: int,
    dollar_blue_repository: ProductWithDollarBluePrices = Depends(
        get_dollar_blue_repository
    ),
):
    try:
        return dollar_blue_repository.get_product(product_id)
    except ValueError:
        return JSONResponse(status_code=400, content="Product not found")
    except Exception:
        return JSONResponse(status_code=500, content="Internal server error")
