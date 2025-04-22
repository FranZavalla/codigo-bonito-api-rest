from datetime import datetime

import requests
from pydantic import BaseModel

from app.layer_1_data_access.connectors.dollar_connector import DollarConnector


class ExchangeRate(BaseModel):
    value_avg: float
    value_sell: float
    value_buy: float


class BluelyticsResponse(BaseModel):
    oficial: ExchangeRate
    blue: ExchangeRate
    oficial_euro: ExchangeRate
    blue_euro: ExchangeRate
    last_update: datetime


class BluelyticsConnector(DollarConnector):
    api = "https://api.bluelytics.com.ar/v2/latest"

    def get_price(self) -> float:
        price_response = requests.get(self.api)
        price_response.raise_for_status()

        json_data = price_response.json()
        try:
            bluelytics_parsed = BluelyticsResponse.model_validate(json_data)
        except Exception as e:
            raise ValueError(f"Error parsing Bluelytics response: {e}")

        return bluelytics_parsed.blue.value_avg
