from fastapi import APIRouter, Depends
from layer_0_db_definition.database_sqlachemy import get_database
from layer_0_db_definition.schema import ProductCreate
from layer_1_repositories.product_sqlachemy import ProductRepository
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("")
def get_products(db: Session = Depends(get_database)):
    try:
        product_repository = ProductRepository(db)
        return product_repository.get_all()
    except Exception as e:
        return {"error": str(e)}


@router.post("")
def create_product(product: ProductCreate, db: Session = Depends(get_database)):
    try:
        product_repository = ProductRepository(db)
        product_repository.create(product)

        return {"message": "Product created"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_database)):
    try:
        product_repository = ProductRepository(db)
        return product_repository.get_by_id(product_id)
    except Exception as e:
        return {"error": str(e)}


@router.put("")
def update_products_price(factor: float, db: Session = Depends(get_database)):
    try:
        product_repository = ProductRepository(db)
        product_repository.update_with_factor(factor)

        return {"message": "Prices updated"}
    except Exception as e:
        return {"error": str(e)}
