# импорт библиотеки
import telebot
import database
import buttons
from telebot import types
# pip install geopy чтобы получить локацию
from geopy.geocoders import Nominatim
# создаём объект бота
# это Frist Bot token
bot = telebot.TeleBot("6563447788:AAGmDrIjgU0jzeiFpgS_QLko57vjTlAN6jY")
# Обработка команды/start
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
users = {}
# database.delete_products()
# database.add_product('Бургер', 30000.0, 10, 'Кайф бургер',
                     #'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOK-9ooVek1Gng3S8I42VyWwGWwE3yAe6hToSbux8d6g&s')
print(database.get_all_products())
print(database.get_pr_id_name())
# print(database.get_exact_product(3))
# print(database.delete_products())
#
def start(message):
    # сохраняем id пользователя
    user_id = message.from_user.id
    # Проверяем наличие пользователя в базе данных
    checker = database.check_user(user_id)
    # если пользователь есть в bd открывает ему меню
    if checker == True:
        bot.send_message(user_id, 'Главное меню', reply_markup=buttons.main_menu())
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

@bot.callback_query_handler(lambda call: call.data in ["products", "cart", "feedback", "plus", "minus",
                                                       "to_cart", "back", "cart", "mm", "order", "clear_cart", "support"])
def for_calls(call):
    user_id = call.message.chat.id
    if call.data == "products":
        actual_product = database.get_pr_id_name()
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Доступные бургеры", reply_markup=buttons.products_menu(actual_product))
    elif call.data == "feedback":
        bot.send_message(user_id, "Напишите ваш отзыв")
        bot.delete_message(user_id, call.message.message_id)
        bot.register_next_step_handler(call.message, feedback_fc)
    elif call.data == "plus":
        current_amount = users[user_id]["pr_count"]
        users[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=buttons.exact_product(current_amount, "plus"))
    elif call.data == "minus":
        current_amount = users[user_id]["pr_count"]
        users[user_id]["pr_count"] -= 1
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message.id,
                                      reply_markup=buttons.exact_product(current_amount, "minus"))
        if current_amount > 1:
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=buttons.exact_product(current_amount, "minus"))
        else:
            pass
    elif call.data == "to_cart":
        to_cart = users[user_id]
        database.add_to_cart(user_id, to_cart["pr_id"], to_cart["pr_name"], to_cart["pr_count"])
        users.pop(user_id)
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Продукт успешно добавлен в корзину")
        actual_product = database.get_pr_id_name()
        bot.send_message(user_id, "Доступные бургеры", reply_markup=buttons.products_menu(actual_product))
    elif call.data == 'back':
        bot.delete_message(user_id, call.message.message_id)
        users.pop(user_id)
        actual_product = database.get_pr_id_name()
        bot.send_message(user_id, "Доступные бургеры", reply_markup=buttons.products_menu(actual_product))
    elif call.data =="cart":
        bot.delete_message(user_id, call.message.message_id)
        user_cart = database.get_user_cart(user_id)
        full_text = f'Ваша корзина: \n \n'
        total_amount = 0
        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]
        full_text += f'\nИтоговая сумма: {total_amount}'
        bot.send_message(user_id, full_text, reply_markup=buttons.get_cart_kb())
    elif call.data == "mm":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, 'Главное меню', reply_markup=buttons.main_menu())
    elif call.data == "clear_cart":
        bot.delete_message(user_id, call.message.message_id)
        database.delete_user_cart(user_id)
        bot.send_message(user_id, 'Ваша корзина очищена')
        bot.send_message(user_id, 'Главное меню', reply_markup=buttons.main_menu())
    elif call.data == "order":
        bot.delete_message(user_id, call.message.message_id)
        user_cart = database.get_user_cart(user_id)
        full_text = f'Новый заказ от юзера {user_id}: \n \n'
        total_amount = 0
        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]
        full_text += f'\nИтоговая сумма: {total_amount}'
        bot.send_message(-1001804805193, full_text)
        database.delete_user_cart(user_id)
        bot.send_message(user_id, "Ваш заказ принят. Ожидайте звонка от курьера")
    elif call.data == "support":
        bot.send_message(user_id, 'Для связи с нами: +9999999 или же @rjjg')
        bot.send_message(user_id, 'Главное меню', reply_markup=buttons.main_menu())

@bot.message_handler(commands=['start'])
def start_get_location(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправьте свою локацию', reply_markup=buttons.get_location())
    bot.register_next_step_handler(message, get_location)
def get_location(message):
    user_id = message.from_user.id
    if message.location:
        # Получение широты и долготы
        latitude = message.location.latitude
        longitude = message.location.longitude
        # преоброазовать всё в адрес
        address = geolocator.reverse((latitude, longitude)).adress
        bot.send_message(user_id, f'{address} - это ваш адрес?')
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку')
        bot.register_next_step_handler(message, get_location)

def feedback_fc(message):
    user_id = message.from_user.id
    bot.send_message(-1001804805193, f"{message.text}\n"
                                     f"Юзер пользователя: {user_id}")
@bot.callback_query_handler(lambda call: int(call.data) in database.get_all_id())
def calls_for_products(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    product = database.get_exact_product(int(call.data))
    users[user_id] = {"pr_id": call.data, "pr_name": product[0], "pr_count": 1}

    bot.send_photo(user_id, photo=product[3], caption=f"{product[0]}\n"
                          f"Цена:{product[1]}\n"
                          f"Описание: {product[2]}\n"
                          f"Выберите количество:", reply_markup=buttons.exact_product())

# чтобы бот работал без остановки добавляем это
bot.infinity_polling()


