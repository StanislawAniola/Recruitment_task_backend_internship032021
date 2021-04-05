import sqlite3
from sqlite3 import Error
from datetime import datetime


class DatabaseClient():
    """
    establish connection to database
    :return: connection object
    """
    def __init__(self, start_date, end_date, currency_name="btc-bitcoin"):
        self.start_date = start_date
        self.end_date = end_date
        self.currency_name = currency_name

    def create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect("./currency_data.db")
            print("connected to the database")
        except Error as e:
            print(e)

        return conn
