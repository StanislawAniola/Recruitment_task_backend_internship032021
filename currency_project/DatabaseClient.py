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

    def check_if_data_in_database(self, conn):
        """
        check if selected range already is in range_date table
        :param conn: Connection object
        """
        sql_get_date = """
                       SELECT currency_name, start_date, end_date
                       FROM range_date 
                       WHERE currency_name='{currency_name}' AND start_date='{start_date}' AND end_date='{end_date}'
                       """
        sql_get_date = sql_get_date.format(currency_name=self.currency_name,
                                           start_date=self.start_date, end_date=self.end_date)

        cursor = conn.cursor()
        try:
            date_in_database = cursor.execute(sql_get_date)
            selected_date_range = False

            for i in date_in_database:
                if len(i) == 3:
                    selected_date_range = True
                    print("Selected date range already in the database")
            return selected_date_range
        except Error as e:
            print(e)
        finally:
            cursor.close()

    @staticmethod
    def insert_data_to_database(conn, currency_data):
        """
        insert currency data to currency_data table
        :param conn: Connection object
        :param currency_data: currency data
        """
        cursor = conn.cursor()
        try:
            for i in currency_data:
                date = datetime.strptime(i["date"], '%Y-%m-%d')

                sqlite_insert_query = """
                                      INSERT INTO currency_data (currency_name, price, date)
                                      SELECT '{name}', {price}, '{date}'
                                      WHERE NOT EXISTS(SELECT * 
                                          FROM currency_data 
                                          WHERE currency_name='{name}' AND date='{date}')
                                      """

                sqlite_insert_query = sqlite_insert_query.format(name=i["name"], price=i["price"], date=date)
                cursor.execute(sqlite_insert_query)
                conn.commit()
            print("Records inserted successfully into table")
        except Error as e:
            print(e)
        finally:
            cursor.close()

    def insert_date_data_range(self, conn):
        """
        insert selected date range into range_date table
        :param conn: Connection object
        """
        sqlite_insert_query = """
                              INSERT INTO range_date (currency_name, start_date, end_date)
                              SELECT '{name}', '{start_date}', '{end_date}'
                              WHERE NOT EXISTS(SELECT * 
                              FROM range_date 
                              WHERE currency_name='{name}' AND start_date='{start_date}' AND end_date='{end_date}')
                              """
        sqlite_insert_query = sqlite_insert_query.format(name=self.currency_name,
                                                         start_date=self.start_date, end_date=self.end_date)

        cursor = conn.cursor()
        try:
            cursor.execute(sqlite_insert_query)
            conn.commit()
            print("Record inserted successfully into SqliteDb_developers table ")
        except Error as e:
            print(e)
        finally:
            cursor.close()

    def get_data_from_database(self, conn):
        """
        get data selected data from currency_data table
        :param conn: Connection object
        """
        sql_get_date = """
                       SELECT currency_name, price, date
                       FROM currency_data 
                       WHERE currency_name='{name}' AND date >= '{start_date}' AND date <= '{end_date}'
                       """
        sql_get_date = sql_get_date.format(name=self.currency_name, start_date=self.start_date, end_date=self.end_date)
        cursor = conn.cursor()
        try:
            result = cursor.execute(sql_get_date)

            data_from_database = []
            for i in result:
                dict_format = {
                    "name": i[0],
                    "price": i[1],
                    "date": i[2][0:10]
                }
                data_from_database.append(dict_format)
            return data_from_database
        except Error as e:
            print(e)
        finally:
            cursor.close()
