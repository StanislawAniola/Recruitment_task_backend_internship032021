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

    def create_table(self, conn):
        """
        create currency_data and range_date tables
        :param conn: Connection object
        """
        sql_create_currency_data_table = """ 
                                         CREATE TABLE IF NOT EXISTS currency_data 
                                         (
                                             id integer PRIMARY KEY,
                                             currency_name VARCHAR(255) NOT NULL,
                                             date DATETIME NOT NULL,
                                             price DOUBLE NOT NULL
                                         ); 
                                         """
        sql_create_range_date_table = """ 
                                 CREATE TABLE IF NOT EXISTS range_date 
                                 (
                                     currency_name VARCHAR(255) NOT NULL,
                                     start_date DATETIME NOT NULL,
                                     end_date DATETIME NOT NULL
                                 ); 
                                 """
        cursor = conn.cursor()
        try:
            cursor.execute(sql_create_currency_data_table)
            cursor.execute(sql_create_range_date_table)
            print("Tables successfully created")
        except Error as e:
            print(e)
        finally:
            cursor.close()
