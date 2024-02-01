# импортируем библиотек телебот, предварительно скачав её через терминал pip instal telebot
import telebot
from telebot import types


# создаем объект нашего бота (мозг бота)
bot = telebot.TeleBot("6563447788:AAGmDrIjgU0jzeiFpgS_QLko57vjTlAN6jY")

def knopka():
    # создаем пространство для кнопки
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # создаем кнопки
    knopka_perevodchik = types.KeyboardButton('Переводчик')
    knopka_nazad = types.KeyboardButton('Назад')
    # вставляем кнопку в пространство
    kb.add(knopka_perevodchik)
    kb.add(knopka_nazad)
    return kb
# @bot.message_handler()
# @bot.message_handler(content_types=["text"])
# def hello(message):
    # print(message.from_user.id)
    # print(message.from_user.is_premium)
    # print(message.from_user.username)
    # print(message.from_user)
    # print(message)
    # user_id = message.from_user.id
    # text = f'Привет, {message.from_user.first_name} ✨'
    # bot.send_message(user_id, text)
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать", reply_markup=knopka())
@bot.message_handler(content_types=['text'])
def start(message):
    user_id = message.from_user.id
    text = message.text
    if text.lower() == 'переводчик':
        bot.send_message(user_id, 'Введите слово для перевода')
    else:
        bot.send_message(user_id, 'Я вас не понимаю')

@bot.message_handler(content_types=["photo"])
def send_photo(message):
    # получаем ID пользователя
    user_id = message.from_user.id
    # сохраняем url Фотки
    photo = "https://mi-store.uz/image/cache/catalog/smart/redminote12progv/redmi_note_12pro_4g_1-650x650.jpg"
    # отправляем фото пользователю
    bot.send_photo(user_id, photo, caption="Дорогой телефон")

# запускаем бесконечный цикл    работы бота
bot.infinity_polling()
