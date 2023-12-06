from telebot import TeleBot
from telebot.types import Message

from config import TOKEN
from config import CURRENCIES
from extensions import APIException
from extensions import PriceConverter


bot = TeleBot(token=TOKEN, parse_mode="markdown")


@bot.message_handler(commands=["start", "help"])
def command_help(message: Message):
    text = (
            "Для работы необходимо отправить боту комманду в следующем формате:\n"
            "<имя валюты цену которой хотите узнать> "
            "<имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def command_values(message: Message) -> None:
    text = "Доступные валюты:\n"
    for currency_name in CURRENCIES.keys():
        text += f"{currency_name}\n"
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def command_convert(message: Message) -> None:
    split_text = message.text.split(" ")
    if len(split_text) != 3:
        bot.reply_to(message, "Слишком много параметров.")
        return

    base, quote, amount = split_text

    try:
        result = PriceConverter.get_price(base, quote, amount)

        text = (
            f"Один {base} стоит {result[0]} {quote}\n"
            f"Цена {amount} {base} равна {result[1]} {quote}"
        )
        bot.reply_to(message, text)
    except APIException as error:
        bot.reply_to(message, str(error))


if __name__ == '__main__':
    bot.polling()
