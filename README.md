# Recruitment_task_backend_internship032021
- author: Stanisław Anioła
- email: aniolastanislaw@gmail.com
- phone: 505822721

## Description
The repository contains functionalities which were built in base of backend internship task requirements.

Script allows to:
1. Communicate with API (https://api.coinpaprika.com)
2. Create Database to store data from API in need of use them more than once
3. Calculate average price of currency by month for given period
4. Find longest consecutive period in which price was increasing
5. Export data for given period in one of selected format csv or json
6. Calculate results for other cryptocurrencies

## Steps to run a script
1. Navigate to folder, to where you want to put a repository
2. Get repository from source
    ```
    git clone https://github.com/StanislawAniola/Recruitment_task_backend_internship032021.git
    ```
3. Navigate to Recruitment_task_backend_internship032021 -> currency_project
4. Activate virtual environment by writing in console:
    ```
    source ../profil_venv/Scripts/activate
    ```

## How to use the script
**Note:** 
1. to each of ***Sample terminal command*** the `--coin` flag can be specified 
with selected currency name i.e. `btc-bitcoin` -> which is selected by default
2. you have to have installed python 3.8.x

---

### Name: Calculate average price
##### Sample terminal command
```
python Main.py --operation=average-price-by-month --start-date=2021-02-03 --end-date=2021-02-15
```
Output format
```
Date      Average price ($)
2021-01   1234.12
2021-02   1252.23
2021-03   1354.55
```

---

### Name: Find longest consecutive period
##### Sample terminal command

```
python Main.py --operation=consecutive-increase --start-date=2021-02-03 --end-date=2021-03-06
```

Output format
```
Longest consecutive period was from 2021-02-24 to 2021-02-28 with increase of $423.54
```

---

### Name: Export data for given period
##### Sample terminal command
```
python Main.py --operation=export-data --start-date=2021-02-03 --end-date=2021-02-10 --format=json --file="test"
```

Data format exported to json:

```
[
  {
    "date": "2021-01-01",
    "price": 1234.56
  },
  {
    "date": "2021-01-02",
    "price": 1234.56
  },
  {
    "date": "2021-01-03",
    "price": 1234.56
  }
]
```

Data format exported to csv:

```
Date         Price
2021-01-01   1234.56
2021-01-02   1235.43
2021-01-03   1234.54
```
