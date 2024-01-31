import telebot
import pycbrf

bot = telebot.TeleBot('6563447788:AAGmDrIjgU0jzeiFpgS_QLko57vjTlAN6jY')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот-конвертер валют. Введите команду /help для получения списка доступных валют.')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Список доступных валют:\nUSD - доллар США\nEUR - евро\nGBP - фунт стерлингов\nCNY - юань')

@bot.message_handler(content_types=['text'])
def convert(message):

    try:
        rate = pycbrf.ExchangeRates().get_rate(message.text.upper(), 'RUB')
    except pycbrf.exceptions.CurrencyNotFoundError:
        bot.send_message(message.chat.id, 'Я не знаю такой валюты. Введите команду /help для получения списка доступных валют.')
        return

    amount = 1000
    converted_amount = round(amount / rate, 2)

    bot.send_message(message.chat.id, f'Курс {message.text.upper()}/RUB: {rate}\n{amount} RUB = {converted_amount} {message.text.upper()}')

bot.polling()
