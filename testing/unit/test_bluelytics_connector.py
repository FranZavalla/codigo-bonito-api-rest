import pytest
from requests.exceptions import HTTPError
from unittest.mock import patch

from testing.mocks.bluelytics_mocks import (
    get_happy_mock_response,
    get_bad_status_mock_response,
    get_bad_parsing_mock_response,
    get_bad_model_mock_response,
)
from app.layer_1_data_access.connectors.bluelytics_connector import (
    BluelyticsConnector,
)


def test_get_prices():
    mock_response = get_happy_mock_response()
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        price = connector.get_price()
        assert price == 1


@pytest.mark.parametrize("avg_value", [0.0005, 1000, 1e9])
def test_get_prices_avg_value(avg_value):
    mock_response = get_happy_mock_response(avg_value)
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        price = connector.get_price()
        assert price == avg_value


def test_get_prices_bad_status():
    mock_response = get_bad_status_mock_response()
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        with pytest.raises(HTTPError):
            connector.get_price()


def test_get_prices_bad_parsing():
    mock_response = get_bad_parsing_mock_response()
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        with pytest.raises(ValueError):
            connector.get_price()


def test_get_prices_bad_model():
    mock_response = get_bad_model_mock_response()
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        with pytest.raises(ValueError):
            connector.get_price()
