# импорт библиотеки
from telebot import types

def get_phone_number():
    # создаем пространство для кнопки
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # создаем саму кнопку
    phone_number = types.KeyboardButton('Поделиться контактом', request_contact=True)
    # добавляем кнопку в пространство
    kb.add(phone_number)
    return kb
