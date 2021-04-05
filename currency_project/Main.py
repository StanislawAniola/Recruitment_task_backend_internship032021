import os, sys
current_path = os.path.abspath('.')
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)

import argparse
from datetime import datetime
from currency_project import APIClient, DatabaseClient, Currency, DataValidation


def arguments_validation(start_date, end_date, currency, file_name):
    """
    check if all validations are correct
    """
    validate = DataValidation.DataValidation(start_date, end_date, currency, file_name)
    validate.check_date_format()
    validate.check_date()
    validate.check_special_characters()
    validate.check_if_file_exists()

    if False in validate.PASS_LIST:
        print("validation of input data not passed, please provide data in correct format")
        sys.exit()


def main():
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('-o', '--operation', type=str, choices=["average-price-by-month",
                                                                "consecutive-increase", "export-data"], required=True)
    parser.add_argument('-sd', '--start-date', type=str, help="start date from where get "
                                                              "currency data, format: YYYY-MM-DD", required=True)
    parser.add_argument('-ed', '--end-date', type=str, help="end date from where get currency data, "
                                                            "format: YYYY-MM-DD", required=True)
    parser.add_argument('-c', '--coin', type=str, help="currency name")
    parser.add_argument('--format', type=str, choices=["json", "csv"], help="choose between json and csv")
    parser.add_argument('--file', type=str, help="choose file name to where save file (can be left unfilled)")

    args = parser.parse_args()
    operation = args.operation
    start_date = args.start_date
    end_date = args.end_date
    currency = args.coin
    export_format = args.format
    file_name = args.file

    if currency is None:
        currency = "btc-bitcoin"

    arguments_validation(start_date, end_date, currency, file_name)

    if file_name is None and export_format is not None:
        currency_name = currency
        currency_start_date = start_date
        currency_end_date = end_date
        file_name = f"{currency_name}_from_{currency_start_date}_to_{currency_end_date}.{export_format}"
    else:
        file_name = f"{file_name}.{export_format}"

    api_client = APIClient.APIClient(start_date, end_date, currency)

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    db_client = DatabaseClient.DatabaseClient(start_date, end_date, currency)

    database_connection = db_client.create_connection()
    db_client.create_table(database_connection)

    result = None
    if db_client.check_if_data_in_database(database_connection):
        result = db_client.get_data_from_database(database_connection)
        print("get data from database")
    else:
        list_of_dicts = api_client.get_currency_from_client()
        db_client.insert_date_data_range(database_connection)
        db_client.insert_data_to_database(database_connection, list_of_dicts)
        result = list_of_dicts
        print("get data from api")

    currency_client = Currency.Currency(result)
    if operation == "average-price-by-month":
        currency_client.average_monthly_price()
    elif operation == "consecutive-increase":
        currency_client.longest_increasing_period()
    elif operation == "export-data" and export_format is not None:
        currency_client.export_currency(export_format, file_name)


main()
