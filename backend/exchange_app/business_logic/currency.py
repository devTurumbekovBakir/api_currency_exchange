import requests
from rest_framework.exceptions import ValidationError


def get_currency_api(from_currency, to_currency):
    url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{from_currency.lower()}/{to_currency.lower()}.json'
    result = requests.get(url=url)
    if result.status_code == 404:
        raise ValidationError('Введенный код валюты не существует')

    data = result.json()
    return data[to_currency.lower()]
