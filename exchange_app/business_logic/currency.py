from datetime import date

import requests

today = date.today()

def get_currency_api(from_currency, to_currency):
    url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{from_currency}/{to_currency}.json'
    result = requests.get(url=url)
    data = result.json()
    return data[to_currency]
