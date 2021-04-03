class Currency():

    def __init__(self, currency_data):
        self.currency_data = currency_data

    def average_monthly_price(self):
        """
        counting monthly average price of given currency
        @return: list of dicts with calculated monthly average price of given currency
        """
        currency_data_list = self.currency_data
        unique_months = set(map(lambda x: x["date"][0:7], currency_data_list))

        average_price_month = []
        for i in unique_months:
            dict_dates = {"Date": i, "Average Price ($)": [x["value"] for x in currency_data_list if x["date"][0:7] == i]}
            average_price_month.append(dict_dates)

        for i in average_price_month:
            i["price"] = sum(i["price"]) / len(i["price"])

        return average_price_month