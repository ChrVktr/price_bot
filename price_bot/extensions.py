import json

import requests

from config import CURRENCIES


class APIException(Exception):
    pass


class PriceConverter:

    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> (float, float):
        try:
            base_ticket = CURRENCIES[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {base}")


        try:
            quote_ticket = CURRENCIES[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество: {amount}")

        req = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticket}&tsyms={quote_ticket}")
        data = json.loads(req.content)

        return data[CURRENCIES[quote]], data[CURRENCIES[quote]] * amount
