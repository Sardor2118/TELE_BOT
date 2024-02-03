import telebot
import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы для хранения информации о пользователях
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER,
                    username TEXT,
                    phone_number TEXT,
                    location TEXT
                )''')
conn.commit()

# Создаем экземпляр бота с токеном
bot = telebot.TeleBot('TOKEN')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Для регистрации введите свое имя:")
    bot.register_next_step_handler(message, process_name_step)


def process_name_step(message):
    username = message.text
    user_id = message.from_user.id
    cursor.execute("INSERT OR REPLACE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()

    bot.send_message(message.chat.id, f"Привет, {username}! Теперь введите свой номер телефона:")
    bot.register_next_step_handler(message, process_phone_step)


def process_phone_step(message):
    phone_number = message.text
    user_id = message.from_user.id
    cursor.execute("UPDATE users SET phone_number = ? WHERE user_id = ?", (phone_number, user_id))
    conn.commit()

    bot.send_message(message.chat.id, "Теперь отправьте свою локацию:")
    bot.register_next_step_handler(message, process_location_step)


def process_location_step(message):
    location = f"latitude: {message.location.latitude}, longitude: {message.location.longitude}"
    user_id = message.from_user.id
    cursor.execute("UPDATE users SET location = ? WHERE user_id = ?", (location, user_id))
    conn.commit()

    bot.send_message(message.chat.id, "Спасибо! Ваша информация принята.")


# Запускаем бота
bot.infinity_polling()
