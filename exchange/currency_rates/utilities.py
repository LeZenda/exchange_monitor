import models
import requests

EXCHANGE_PRICES_API = 'https://api.cryptonator.com/api/ticker/'


def check_exchange_currencies(currencies):
    """
    check if the currencies pair is valid for imports

    :param currencies: receive string that consists of two currencies names
    :return: True is the string is valid
    """

    r = requests.get(EXCHANGE_PRICES_API+currencies)
    if r.status_code == 200 and r.json()['success'] is True:
        return True
    return False


def update_prices_for_exchanges():
    """
        Cycles through all Exchange currencies and saves any new prices
    """
    exch_currs = models.ExchangeCurrencies.objects.filter(active=True)

    for exch_curr in exch_currs:

        r = requests.get(EXCHANGE_PRICES_API + exch_curr.currencies)
        if r.status_code == 200:
            resp = r.json()
            if resp['success'] is True and exch_curr.last_price() != float(resp['ticker']['price']):
                models.ExchangeRates.objects.create(currencies=exch_curr, price=float(resp['ticker']['price']))
