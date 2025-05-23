import pytest

from requests.exceptions import HTTPError

from app.layer_1_data_access.connectors.bluelytics_connector import (
    BluelyticsConnector,
)
from testing.mocks.bluelytics_mocks import (
    HappyMockResponse,
    BadModelMockResponse,
    BadParsingMockResponse,
    BadStatusMockResponse,
)


def test_get_prices(monkeypatch):
    monkeypatch.setattr("requests.get", lambda url: HappyMockResponse())
    connector = BluelyticsConnector()
    price = connector.get_price()
    assert price == 1


@pytest.mark.parametrize("avg_value", [0.05, 1000, 1e9])
def test_get_prices_avg_value(monkeypatch, avg_value):
    monkeypatch.setattr("requests.get", lambda url: HappyMockResponse(avg_value))
    connector = BluelyticsConnector()
    price = connector.get_price()
    assert price == avg_value


def test_get_prices_bad_status(monkeypatch):
    monkeypatch.setattr("requests.get", lambda url: BadStatusMockResponse())
    connector = BluelyticsConnector()
    with pytest.raises(HTTPError):
        connector.get_price()


def test_get_prices_bad_parsing(monkeypatch):
    monkeypatch.setattr("requests.get", lambda url: BadParsingMockResponse())
    connector = BluelyticsConnector()
    with pytest.raises(ValueError):
        connector.get_price()


def test_get_prices_bad_model(monkeypatch):
    monkeypatch.setattr("requests.get", lambda url: BadModelMockResponse())
    connector = BluelyticsConnector()
    with pytest.raises(ValueError):
        connector.get_price()
