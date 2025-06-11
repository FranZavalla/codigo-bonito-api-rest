from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.layer_1_data_access.repositories.product_abstract import (
    AbstractProductRepository,
    CreateProductData,
)
from app.layer_2_logic.factory import get_product_repository

router = APIRouter()


@router.get("")
def get_products(
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        products = product_repository.get_all()
        json_products = [product.model_dump() for product in products]
        return JSONResponse(status_code=200, content={"detail": json_products})
    except Exception:
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )


@router.post("")
def create_product(
    product: CreateProductData,
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        product_repository.create(product)

        return JSONResponse(status_code=201, content={"detail": "Product created"})
    except Exception:
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )


@router.get("/{product_id}")
def get_product(
    product_id: int,
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        product = product_repository.get_by_id(product_id)
        json_product = product.model_dump()
        return JSONResponse(status_code=200, content=json_product)
    except ValueError:
        return JSONResponse(status_code=404, content={"detail": "Product not found"})
    except Exception:
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )


@router.put("")
def update_products_price(
    factor: float,
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        product_repository.update_with_factor(factor)

        return JSONResponse(status_code=200, content={"detail": "Products updated"})
    except Exception:
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )
