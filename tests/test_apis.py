import datetime
import pytest
import requests
from capturing_data_digital_currencies.mercado_bitcoin.apis import DaySummaryApi, TradesApi, MercadoBitcoinApi
from unittest.mock import patch


class TestDaySummaryApi:
    @pytest.mark.parametrize(
        "coin, date, expected",
        [
            ("BTC", datetime.date(2021, 6, 1), "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/1"),
            ("ETH", datetime.date(2022, 6, 1), "https://www.mercadobitcoin.net/api/ETH/day-summary/2022/6/1"),
            ("LTC", datetime.date(2022, 7, 1), "https://www.mercadobitcoin.net/api/LTC/day-summary/2022/7/1"),
            ("BCH", datetime.date(2022, 7, 1), "https://www.mercadobitcoin.net/api/BCH/day-summary/2022/7/1"),
        ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryApi(coin=coin)
        actual = api._get_endpoint(date=date)
        assert actual == expected


class TestTradesApi:
    @pytest.mark.parametrize(
        "coin, date_from, date_to, expected",
        [
            ("TEST", datetime.datetime(2019, 1, 1), datetime.datetime(2019, 1, 2),
             "https://www.mercadobitcoin.net/api/TEST/trades/1546311600/1546398000"),
            ("TEST", datetime.datetime(2020, 12, 31), datetime.datetime(2021, 1, 1),
             "https://www.mercadobitcoin.net/api/TEST/trades/1609383600/1609470000"),
            ("TEST", datetime.datetime(2022, 4, 12), datetime.datetime(2022, 4, 13),
             "https://www.mercadobitcoin.net/api/TEST/trades/1649732400/1649818800"),
            ("TEST", None, None,
             "https://www.mercadobitcoin.net/api/TEST/trades"),
            ("TEST", None, datetime.datetime(2022, 4, 13),
             "https://www.mercadobitcoin.net/api/TEST/trades"),
            ("TEST", datetime.datetime(2022, 4, 12), None,
             "https://www.mercadobitcoin.net/api/TEST/trades/1649732400"),

        ]
    )
    def test_get_endpoint(self, coin, date_from, date_to, expected):
        actual = TradesApi(coin=coin)._get_endpoint(date_from=date_from, date_to=date_to)
        assert actual == expected

    def test_get_endpoint_date_from_greater_date_to(self):
        with pytest.raises(RuntimeError):
            TradesApi(coin='TEST')._get_endpoint(date_from=datetime.datetime(2022, 4, 15),
                                                 date_to=datetime.datetime(2022, 4, 13))

    @pytest.mark.parametrize(
        "date, expected",
        [
            (datetime.datetime(2019, 1, 1), 1546311600),
            (datetime.datetime(2019, 1, 2), 1546398000),
            (datetime.datetime(2020, 12, 31), 1609383600),
            (datetime.datetime(2021, 1, 1), 1609470000),
            (datetime.datetime(2022, 4, 12), 1649732400),
            (datetime.datetime(2022, 4, 13), 1649818800),
        ]
    )
    def test_get_unix_date(self, date, expected):
        actual = TradesApi(coin='Test')._get_unix_date(date=date)
        assert actual == expected


@pytest.fixture()
@patch("apis.MercadoBitcoinApi.__abstractmethod__", set())
def fixture_mercado_bitcoin_api():
    return MercadoBitcoinApi(
        coin='Test'
    )


def mocked_requests_get(*args):
    class MockResponse(requests.Request):
        def __init__(self, json_data, status_code):
            super().__init__()
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self) -> None:
            if self.status_code != 200:
                raise Exception

    if args[0] == 'valid_enpoint':
        return MockResponse(json_data={"key": "value"}, status_code=200)
    else:
        return MockResponse(json_data=None, status_code=404)


class TestMercadoBitcoinApi:
    @patch("requests.get")
    @patch("apis.MercadoBitcoinApi._get_endpoint", return_value="valid_endpoint")
    def test_get_data_requests_is_called(self, mock_requests, fixture_mercado_bitcoin_api):
        fixture_mercado_bitcoin_api._get_endpoint()
        mock_requests.assert_called_once_with("valid_endpoint")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("apis.MercadoBitcoinApi._get_endpoint", return_value="valid_endpoint")
    def test_get_data_with_valid_endpoint(self, fixture_mercado_bitcoin_api):
        actual = fixture_mercado_bitcoin_api.get_data()
        expected = {"key": "value"}
        assert actual == expected

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("apis.MercadoBitcoinApi._get_endpoint", return_value="invalid_endpoint")
    def test_get_data_with_invalid_endpoint(self, fixture_mercado_bitcoin_api):
        with pytest.raises(Exception):
            fixture_mercado_bitcoin_api.get_data()
