from datetime import datetime
import os, sys


class DataValidation():

    PASS_LIST = []

    def __init__(self, start_date, end_date, currency_name, file_name=None, operation=None):
        self.start_date = start_date
        self.end_date = end_date
        self.currency_name = currency_name
        self.file_name = file_name
        self.operation = operation

    def check_date_format(self):
        """
        check if provided date format is correct
        """
        pass_check = False
        try:
            datetime.strptime(self.start_date, '%Y-%m-%d')
            datetime.strptime(self.end_date, '%Y-%m-%d')
            pass_check = True
        except:
            print("please provide date format as YYYY-MM-DD")
        self.PASS_LIST.append(pass_check)

    def check_date(self):
        """
        check if end_date is bigger or equal start_date
        """
        pass_check = True

        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')

        if self.PASS_LIST[0]:

            if start_date > end_date:
                pass_check = False
                print("please make sure to provide end_date bigger than start_date")

        if self.operation == "consecutive-increase" and start_date == end_date:
            print("start_date equal end_date please get at least one day difference between dates")
            pass_check = False

        if self.operation == "consecutive-increase" and start_date == datetime.now():
            print("start_date should be earlier date")
            pass_check = False

        self.PASS_LIST.append(pass_check)


    def check_special_characters(self):
        """
        check if provided file name contains special characters
        """
        wrong_characters = '[@!#$%^&*()<>?/\|}{~:]'
        pass_check = True
        if self.file_name is not None:
            for i in self.file_name:
                if i in wrong_characters:
                    pass_check = False
                    print("one of --file argument is a special character")
        self.PASS_LIST.append(pass_check)

    def check_if_file_exists(self):
        """
        check if provided file name already exists in base directory
        """
        try:
            file_json = self.file_name + ".json"
            file_csv = self.file_name + ".csv"

            if os.path.isfile(file_json) or os.path.isfile(file_csv):
                print("File name exists, change file name or file can be filled with new data if "
                      "the file extension is not different")

                question = 0
                while question < 1:
                    choice = input("if yes, press 'y' else press 'n': ")
                    if choice == "y":
                        break
                    elif choice != "y" and choice != "n" or choice == "n":
                        print("interrupting a program, please change file name.")
                        sys.exit()

                    question += 1
        except:
            print("")
