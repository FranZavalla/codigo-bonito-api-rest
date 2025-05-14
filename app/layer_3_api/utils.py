from fastapi import Depends
from sqlalchemy.orm import Session

from app.layer_0_db_definition.database_sqlalchemy import get_database
from app.layer_1_data_access.repositories.Product.utils import select_product_repository


def get_product_repository(db: Session = Depends(get_database)):
    return select_product_repository(db)
