from datetime import datetime
from requests.exceptions import HTTPError
from unittest.mock import MagicMock


def get_happy_mock_response(value_avg=1):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "oficial": {"value_avg": 1, "value_sell": 1, "value_buy": 1},
        "blue": {"value_avg": value_avg, "value_sell": 1, "value_buy": 1},
        "oficial_euro": {"value_avg": 1, "value_sell": 1, "value_buy": 1},
        "blue_euro": {"value_avg": 1, "value_sell": 1, "value_buy": 1},
        "last_update": datetime.now(),
    }

    return mock_response


def get_bad_status_mock_response():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Bad status", response=mock_response
    )
    return mock_response


def get_bad_parsing_mock_response():
    mock_response = MagicMock()
    mock_response.json.side_effect = ValueError("Error parsing Bluelytics response")
    return mock_response


def get_bad_model_mock_response():
    mock_response = MagicMock()
    mock_response.json.return_value = {"bad_model": "bad_model"}
    return mock_response
