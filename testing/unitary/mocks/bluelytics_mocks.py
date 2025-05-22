from datetime import datetime
from requests.exceptions import HTTPError

from app.layer_1_data_access.connectors.bluelytics_connector import (
    BluelyticsResponse,
    ExchangeRate,
)


class HappyMockResponse:
    def __init__(self, value_avg=1):
        self.value_avg = value_avg

    def raise_for_status(self):
        pass

    def json(self):
        exchange_rate = ExchangeRate(
            value_avg=self.value_avg, value_sell=1, value_buy=1
        )
        return BluelyticsResponse(
            oficial=exchange_rate,
            blue=exchange_rate,
            oficial_euro=exchange_rate,
            blue_euro=exchange_rate,
            last_update=datetime.now(),
        )


class BadStatusMockResponse:
    def raise_for_status(self):
        raise HTTPError("Bad status", response=self)


class BadParsingMockResponse:
    def raise_for_status(self):
        pass

    def json(self):
        raise ValueError("Error parsing Bluelytics response")


class BadModelMockResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"bad_model": "bad_model"}
