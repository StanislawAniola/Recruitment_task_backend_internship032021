import sys
from functools import wraps
import json
import csv


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

    def longest_increasing_period(self):
        """
        calculate average price of currency by month for given period
        """
        currency_data_list = self.currency_data

        def find_longest_upward_trend(upward_trends_list):
            """
            find longest upward trend
            :param upward_trends_list: upward trends list
            """
            @wraps(upward_trends_list)
            def wrapper(*args, **kwargs):
                up_tren_list = upward_trends_list(*args, **kwargs)
                if len(up_tren_list) == 0:
                    print("get wider range of dates")
                    sys.exit()

                max = upward_trends_list(*args, **kwargs)[0]
                for i in up_tren_list:
                    if len(i["price"]) > len(max["price"]):
                        max = i
                longest_upward_trend_list = [x for x in up_tren_list if len(x["price"]) == len(max["price"])]
                return longest_upward_trend_list

            return wrapper

        def create_list_of_upward_trends(inflection_points_list):
            """
            find all upward trends in data from api or database in base of inflection points
            :param: inflection_points_list: inflection points list
            :return: list of all upward trends in list
            """
            @wraps(inflection_points_list)
            def wrapper(*args, **kwargs):
                inflection_points_obj = inflection_points_list(*args, **kwargs)
                start_of_upward_trends = [i for i in range(0, len(inflection_points_obj)) if
                                          (inflection_points_obj[i] != "break" and
                                           inflection_points_obj[i - 1] == "break") or
                                          (i == 0 and inflection_points_obj[i] != "break")]

                upward_trends_list = []
                for i in start_of_upward_trends:
                    inflection_dict_element = {"start_date": currency_data_list[i]["date"], "price": []}
                    for j in range(i, len(inflection_points_obj)):
                        if inflection_points_obj[j] != "break":
                            inflection_dict_element["price"].append(currency_data_list[j]["price"])
                            inflection_dict_element["end_date"] = currency_data_list[j]["date"]
                        elif inflection_points_obj[j] == "break":
                            inflection_dict_element["price"].append(currency_data_list[j]["price"])
                            inflection_dict_element["end_date"] = currency_data_list[j]["date"]
                            break
                    upward_trends_list.append(inflection_dict_element)
                return upward_trends_list

            return wrapper

        def find_inflection_points(currency_raw_data):
            """
            find inflection points in given data list of dicts
            :param currency_raw_data: currency data directly from api or database
            :return: inflection points in given currency data
            """
            @wraps(currency_raw_data)
            def wrapper(*args, **kwargs):
                currency_data_to_process = currency_raw_data(*args, **kwargs)
                inflection_points_list = []
                for i in range(0, len(currency_data_to_process)):
                    if i + 1 == len(currency_data_to_process):
                        break
                    if currency_data_to_process[i]["price"] < currency_data_to_process[i + 1]["price"]:
                        inflection_points_list.append(currency_data_to_process[i]["price"])
                    else:
                        inflection_points_list.append("break")
                return inflection_points_list

            return wrapper

        @find_longest_upward_trend
        @create_list_of_upward_trends
        @find_inflection_points
        def result_func(data_to_process):
            return data_to_process

        result = result_func(currency_data_list)

        def display_longest_increasing_period(data_to_print):
            """
            display longest upward trend increasing period
            :param data_to_print: result data to print
            """
            for i in data_to_print:
                start_date = i["start_date"]
                end_date = i["end_date"]
                price = round((i["price"][-1] - i["price"][0]), 2)
                print(f'Longest consecutive period was from {start_date} to {end_date} with increase of ${price}')

        display_longest_increasing_period(result)

    def export_currency(self, export_structure, file_name):
        """
        export currency in csv or json
        :param export_structure: json or csv
        :param file_name: name of the file to write data
        """
        data_to_export = self.currency_data

        if export_structure == "json":
            for i in data_to_export:
                i.pop('name', None)
                i["price"] = round(i["price"], 2)

            dict_order_key = map(lambda x: {"date": x["date"], "price": x["price"]}, data_to_export)

            with open(f'./{file_name}', 'w', newline='') as outfile:
                json.dump(list(dict_order_key), outfile, indent=4, separators=(',', ': '))
            print(f"{file_name} has been generated")
        elif export_structure == "csv":
            keys = data_to_export[0].keys()
            column_names = list(keys)[1:]
            date_col = column_names[1].capitalize()
            price_col = 9*" " + column_names[0].capitalize()
            with open(f'./{file_name}', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=[date_col, price_col], delimiter=",")
                dict_writer.writeheader()

                for data in data_to_export:
                    date = data["date"]
                    price = "   {0:10}".format(data["price"])

                    dict_writer.writerow({date_col: date, price_col: price})
            print(f"{file_name} has been generated")
