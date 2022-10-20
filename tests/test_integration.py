import datetime

from capturing_data_digital_currencies.mercado_bitcoin.apis import DaySummaryApi


class TestDaySummaryApi:
    def test_get_data(self):
        actual = DaySummaryApi(coin='BTC').get_data(date=datetime.date(2021, 1, 1))
        expected = {'amount': 4824,
                    'avg_price': 152947.34346135,
                    'closing': 153458.29999999,
                    'date': '2021-01-01',
                    'highest': 153975,
                    'lowest': 151539,
                    'opening': 152700.00002,
                    'quantity': '82.27265844',
                    'volume': '12583384.54790148'}

        assert actual == expected

    def test_get_data_better(self):
        actual = DaySummaryApi(coin='BTC').get_data(date=datetime.date(2021, 1, 1)).get("date")
        expected = '2021-01-01'

        assert actual == expected
