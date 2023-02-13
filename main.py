import telebot
import requests
import json

from config import TOKEN, currency
from extension import ConvertionException, Convertor_Money

class ConvertionException(Exception):
    pass

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start',])
def start(message: telebot.types.Message):
    text = 'Приветствуем Вас в конвертере валют \n Для вызова помощника наберите: /help'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help',])
def start(message: telebot.types.Message):
    text = ' Чтобы начать работу введите комманду боту в следующем формате:\n \
 <имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты> \
\n Увидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values',])
def values (message: telebot.types.Message):
    text= 'Доступные валюты:'
    for i in currency.keys():
        text='\n'.join((text, i))
    bot.send_message(message.chat.id,text )

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров!')
        
        quote, base,amount = values
        new_price = Convertor_Money.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.send_message(message.chat.id,new_price)

bot.polling(none_stop=True)