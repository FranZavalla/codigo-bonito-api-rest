from sqlalchemy.orm import Session

from app.layer_0_db_definition.database_sqlalchemy import get_database
from app.layer_1_data_access.connectors.bluelytics_connector import \
    BluelyticsConnector
from app.layer_1_data_access.repositories.Product.product_abstract import \
    AbstractProductRepository
from app.layer_1_data_access.repositories.Product.utils import \
    select_product_repository
from app.layer_2_logic.product_with_dollar_blue import \
    ProductWithDollarBluePrices


def get_product_repository() -> AbstractProductRepository:
    with get_database() as db:
        return select_product_repository(db)


def get_dollar_blue_repository() -> ProductWithDollarBluePrices:
    product_repository = get_product_repository()
    dollar_blue_connector = BluelyticsConnector()
    return ProductWithDollarBluePrices(product_repository, dollar_blue_connector)
