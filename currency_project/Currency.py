class Currency():

    def __init__(self, currency_data):
        self.currency_data = currency_data

    def average_monthly_price(self):
        """
        calculate monthly currency price
        """
        currency_data_list = self.currency_data
        unique_list_of_dates = set(map(lambda x: x["date"][0:7], currency_data_list))

        currency_date_list = []
        for i in unique_list_of_dates:
            dict_dates = {"date": i,
                          "price": [x["price"] for x in currency_data_list if x["date"][0:7] == i]}
            currency_date_list.append(dict_dates)

        date_col = 'Date'
        avg_price_col = 'Average price ($)'
        print('{0:10}  {1}'.format(date_col, avg_price_col))
        for i in currency_date_list:
            i["price"] = round(sum(i["price"])/len(i["price"]), 2)
            print('{0:10}  {1}'.format(i["date"], i["price"]))