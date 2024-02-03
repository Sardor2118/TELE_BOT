# импорт библиотеки
import telebot
import database
import buttons
from telebot import types
# создаём объект бота
# это Frist Bot token
bot = telebot.TeleBot("6563447788:AAGmDrIjgU0jzeiFpgS_QLko57vjTlAN6jY")
# Обработка команды/start
@bot.message_handler(commands=['start'])
def start(message):
    # сохраняем id пользователя
    user_id = message.from_user.id
    # Проверяем наличие пользователя в базе данных
    checker = database.check_user(user_id)
    # если пользователь есть в bd открывает ему меню
    if checker == True:
        bot.send_message(user_id, 'Главное меню')
    # если пользователя нет в бд, начинаем регистрацию
    elif checker == False:
        # отправляем ответ на команду старт
        bot.send_message(user_id, "Добро пожаловать в наш бот доставки еды TEST. \n"
                                  "Начнём регистрацию. Введите своё имя")
        bot.register_next_step_handler(message, registration)
def registration(message):
    user_id = message.from_user.id
    name = message.text
    # просим отправить номер и крикрепляем кнопку
    bot.send_message(user_id, "Отправьте свой номер телефона", reply_markup=buttons.get_phone_number())
    # переход на следуюищй этап получения номера и сохранение имени
    bot.register_next_step_handler(message, get_number, name)
def get_number(message, name):
    user_id = message.from_user.id
    # сохраняем в переменную номер
    # проверяем в каком формате отправлен номер
    # если через кнопку
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, 'Вы успешно зарегестрировались!', reply_markup=types.ReplyKeyboardRemove())
        database.add_user(user_id=user_id, user_name=name, user_phone_number=phone_number)
        print(database.get_users())
    # если номер записан вручную возвращаем его в эту же функцию
    else:
        bot.send_message(user_id, 'Отправьте свой номер через кнопку')
        bot.register_next_step_handler(message, get_number, name)
# bot.register_next_step_handler(message, следующая функция, аргументы)
    print(message.contact)

# чтобы бот работал без остановки добавляем это
bot.infinity_polling()
