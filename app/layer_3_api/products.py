from fastapi import APIRouter, Depends


from app.layer_0_db_definition.schema import CreateProductData
from app.layer_1_data_access.repositories.Product.product_abstract import (
    AbstractProductRepository,
)
from app.layer_3_api.utils import get_product_repository

router = APIRouter()


@router.get("")
def get_products(
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        return product_repository.get_all()
    except Exception as e:
        return {"error": str(e)}


@router.post("")
def create_product(
    product: CreateProductData,
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        product_repository.create(product)

        return {"message": "Product created"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/{product_id}")
def get_product(
    product_id: int,
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        return product_repository.get_by_id(product_id)
    except Exception as e:
        return {"error": str(e)}


@router.put("")
def update_products_price(
    factor: float,
    product_repository: AbstractProductRepository = Depends(get_product_repository),
):
    try:
        product_repository.update_with_factor(factor)

        return {"message": "Prices updated"}
    except Exception as e:
        return {"error": str(e)}
