import requests


class CurrencyRate:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        # first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]

            # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


def get_rates():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyRate(url)
    return converter.currencies


def get_latest_rate(from_currency, to_currency, amount=None):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyRate(url)
    if amount is None:
        amount = 100
    return str(converter.convert(from_currency, to_currency, amount))




