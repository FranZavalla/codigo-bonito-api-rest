from typing import Optional

from sqlalchemy.orm import Session

from app.settings import settings


def select_product_repository(db: Optional[Session] = None):
    """
    Returns the appropriate product repository based on the configuration settings.

    Args:
        db (Session, optional): The database session to use. Defaults to None.

    Returns:
        Union[SQLARepo, PonyRepo]: An instance of the appropriate product repository.
    """
    if settings.ORM == "sqlalchemy":
        from app.layer_1_data_access.repositories.Product.product_sqlachemy import \
            SQLAlchemyProductRepository

        return SQLAlchemyProductRepository(db)
    elif settings.ORM == "ponyorm":
        from app.layer_1_data_access.repositories.Product.product_pony import \
            PonyProductRepository

        return PonyProductRepository()
    else:
        raise ValueError("Invalid ORM in settings.")
