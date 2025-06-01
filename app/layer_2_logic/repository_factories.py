from typing import Optional
from sqlalchemy.orm import Session

from app.layer_0_db_definition.database_sqlalchemy import get_database
from app.layer_1_data_access.connectors.bluelytics_connector import BluelyticsConnector
from app.layer_2_logic.product_with_dollar_blue import ProductWithDollarBluePrices
from app.layer_1_data_access.repositories.product_abstract import (
    AbstractProductRepository,
)
from app.settings import settings


def select_product_repository(
    db: Optional[Session] = None,
) -> AbstractProductRepository:
    """
    Returns the appropriate product repository based on the configuration settings.

    Args:
        db (Session, optional): The database session to use. Defaults to None.

    Returns:
        Union[SQLARepo, PonyRepo]: An instance of the appropriate product repository.
    """
    if settings.ORM == "sqlalchemy":
        from app.layer_1_data_access.repositories.product_sqlachemy import (
            SQLAlchemyProductRepository,
        )

        return SQLAlchemyProductRepository(db)
    elif settings.ORM == "ponyorm":
        from app.layer_1_data_access.repositories.product_pony import (
            PonyProductRepository,
        )

        return PonyProductRepository()
    else:
        raise ValueError("Invalid ORM in settings.")


def get_product_repository() -> AbstractProductRepository:
    db: Session = get_database()
    return select_product_repository(db)


def get_dollar_blue_repository() -> ProductWithDollarBluePrices:
    product_repository = get_product_repository()
    dollar_blue_connector = BluelyticsConnector()
    return ProductWithDollarBluePrices(product_repository, dollar_blue_connector)
