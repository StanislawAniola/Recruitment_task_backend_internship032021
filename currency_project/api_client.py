import requests


class APIClient():

    API_BASE_URL = "https://api.coinpaprika.com/v1/coins/"

    def __init__(self, start_date, end_date, currency_id="btc-bitcoin"):
        self.start_date = start_date
        self.end_date = end_date
        self.currency_id = currency_id

    def get_currency_from_api(self):
        """
        sends request to API
        @return: raw data from request
        """
        return requests.get("{0}/{1}/ohlcv/historical?start={2}&end={3}".format(self.API_BASE_URL, self.currency_id,
                                                                                self.start_date, self.end_date))

    def get_currency_from_client(self):
        """
        get data from request
        @return: list of dicts with data from request
        """
        client_result = self.get_currency_from_api().json()

        currency_list = []
        for i in client_result:
            currency_dict = {"name": self.currency_id,
                             "value": i["close"],
                             "date": i["time_open"][0:10]}
            currency_list.append(currency_dict)

        return currency_list
