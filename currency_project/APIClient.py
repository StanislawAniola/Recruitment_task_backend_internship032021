import requests


class APIClient():

    API_BASE_URL = "https://api.coinpaprika.com/v1/coins/"

    def __init__(self, start_date, end_date, currency_id="btc-bitcoin"):
        self.start_date = start_date
        self.end_date = end_date
        self.currency_id = currency_id

    def get_currency_from_api(self):
        """
        provide connection to API
        """
        response = requests.get("{0}/{1}/ohlcv/historical?start={2}&end={3}".format(self.API_BASE_URL, self.currency_id,
                                                                                    self.start_date, self.end_date))
        status = response.status_code
        if status == 200:
            print("connection established")
        else:
            print("connection error")

        return response

    def get_currency_from_client(self):
        """
        get data from provided connection to API
        :return: data from api
        """
        client_result = self.get_currency_from_api().json()

        currency_list = []
        for i in client_result:
            currency_dict = {"name": self.currency_id, "price": i["close"], "date": i["time_open"][0:10]}
            currency_list.append(currency_dict)

        return currency_list
