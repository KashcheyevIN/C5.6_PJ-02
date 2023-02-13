import json
import requests
from config import currency

class ConvertionException(Exception):
    pass


class Convertor_Money:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f"Валюта {base} не найдена!")

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f"Валюта {quote} не найдена!")

       
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}!')
        
       
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
                
        resp = json.loads(r.content) # конвертируем в читаемый формат
        new_price = resp[quote_ticker] * amount #убираем лишнее и умножаем на количество валюты
        new_price = round(new_price, 3) #оставляем 3 знака
        message =  f"Цена {amount} {base} в {quote} : {new_price}"
        return message
