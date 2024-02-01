# импортируем библиотеку
import sqlite3
from datetime import datetime
# создаем подключение/файл
connection = sqlite3.connect('dostavka.db')
# среда или перевдочик
sql = connection.cursor()
# создаем таблицу users
sql.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT, phone_number TEXT, reg_date DATETIME);')

def add_user(user_id, user_name, user_phone_number):
    # создаем подключение/файл
    connection = sqlite3.connect('dostavka.db')
    # среда или перевдочик
    sql = connection.cursor()
    # сохраняем данные из бота
    sql.execute('INSERT INTO users (user_id, name, phone_number, reg_date) VALUES (?, ?, ?, ?);',
                (user_id, user_name, user_phone_number, datetime.now()))
    connection.commit()
def get_users():
    # создаем подключение/файл
    connection = sqlite3.connect('dostavka.db')
    # среда или перевдочик
    sql = connection.cursor()
    # Получение всех пользователей
    users = sql.execute('SELECT * FROM users;').fetchall()
    # Передаем результат
    return users
def check_user(user_id):
    # проверяем зарегался ли пользователь, чтобы не смог повторно
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()
    checker = sql.execute("SELECT user_id FROM users WHERE user_id = ?;", (user_id, )).fetchone()
    # если пользователь есть, то возвращаем True
    if checker:
        return True
    # если пользователь нет - False
    else:
        return False