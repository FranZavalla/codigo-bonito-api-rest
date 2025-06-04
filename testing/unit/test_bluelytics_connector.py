from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from app.layer_1_data_access.connectors.bluelytics_connector import \
    BluelyticsConnector
from testing.mocks.bluelytics_mocks import (get_bad_model_mock_response,
                                            get_bad_parsing_mock_response,
                                            get_bad_status_mock_response,
                                            get_happy_mock_response)


def test_get_prices_return_avg_value_on_success():
    mock_response = get_happy_mock_response()
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        price = connector.get_price()
        assert price == 1


def test_get_prices_call_once_on_success():
    mock_response = get_happy_mock_response()
    with patch("requests.get", return_value=mock_response) as mock_get:
        connector = BluelyticsConnector()
        connector.get_price()
        mock_get.assert_called_once_with(connector.endpoint)


@pytest.mark.parametrize("avg_value", [0.0005, 1000, 1e9])
def test_get_prices_success_edge_cases(avg_value):
    mock_response = get_happy_mock_response(avg_value)
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        price = connector.get_price()
        assert price == avg_value


def test_get_prices_raises_http_error_on_bad_status():
    mock_response = get_bad_status_mock_response()
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        with pytest.raises(HTTPError):
            connector.get_price()


def test_get_prices_raises_value_error_on_bad_parsing():
    mock_response = get_bad_parsing_mock_response()
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        with pytest.raises(ValueError):
            connector.get_price()


def test_get_prices_raises_value_error_on_bad_model():
    mock_response = get_bad_model_mock_response()
    with patch("requests.get", return_value=mock_response):
        connector = BluelyticsConnector()
        with pytest.raises(ValueError):
            connector.get_price()
