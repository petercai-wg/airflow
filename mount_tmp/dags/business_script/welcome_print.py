import datetime

import requests

def print_welcome():

    print("Welcome to Airflow!")


def print_date():

    print("Today is {}".format(datetime.datetime.today().date()))


def print_random_quote():

    response = requests.get("https://stoic.tekloon.net/stoic-quote")

    quote = response.json()["data"]["quote"]

    print(f'Quote of the day: {quote}')