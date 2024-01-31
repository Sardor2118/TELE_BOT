# Импортируем нужные модули
import telebot
from googletrans import Translator
import wikipedia

# Создаем бота и указываем токен
bot = telebot.TeleBot('6260300152:AAG7EchVpa27hnIhm3tCWEGK8_1ZJcc7OnA')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # Создаем клавиатуру с двумя кнопками
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Перевод')
    button2 = telebot.types.KeyboardButton('Википедия')
    keyboard.add(button1, button2)

    # Отправляем сообщение с приветствием и клавиатурой
    bot.send_message(message.chat.id, 'Привет! Я бот помощник по переводу или нахождение информаций👍🏻.', reply_markup=keyboard)


# Обработчик кнопки "Перевод"
@bot.message_handler(func=lambda message: message.text == 'Перевод')
def translate_message(message):
    # Отправляем сообщение с запросом языков
    bot.send_message(message.chat.id, 'Введите язык, с которого нужно перевести:')

    # Устанавливаем состояние пользователя в "ожидание языка исходного текста"
    bot.register_next_step_handler(message, get_source_language)


# Функция получения языка исходного текста
def get_source_language(message):
    # Сохраняем язык исходного текста в переменную состояния пользователя
    bot.current_state(chat=message.chat.id, state='source_language').update({'source_language': message.text})

    # Отправляем сообщение с запросом языка перевода
    bot.send_message(message.chat.id, 'Введите язык, на который нужно перевести:')

    # Устанавливаем состояние пользователя в "ожидание языка перевода"
    bot.register_next_step_handler(message, get_target_language)


# Функция получения языка перевода
def get_target_language(message):
    # Сохраняем язык перевода в переменную состояния пользователя
    bot.current_state(chat=message.chat.id, state='target_language').update({'target_language': message.text})

    # Отправляем сообщение с запросом текста для перевода
    bot.send_message(message.chat.id, 'Введите текст для перевода:')

    # Устанавливаем состояние пользователя в "ожидание текста для перевода"
    bot.register_next_step_handler(message, translate_text)


# Функция перевода текста
def translate_text(message):
    # Получаем язык исходного текста из переменной состояния пользователя
    source_language = bot.current_state(chat=message.chat.id, state='source_language')['source_language']

    # Получаем язык перевода из переменной состояния пользователя
    target_language = bot.current_state(chat=message.chat.id, state='target_language')['target_language']

    # Создаем объект переводчика и переводим текст
    translator = Translator()
    translated_text = translator.translate(message.text, src=source_language, dest=target_language).text

    # Отправляем сообщение с переведенным текстом
    bot.send_message(message.chat.id, translated_text)


# Обработчик кнопки "Википедия"
@bot.message_handler(func=lambda message: message.text == 'Википедия')
def wikipedia_message(message):
    # Отправляем сообщение с запросом темы для поиска на Википедии
    bot.send_message(message.chat.id, 'Введите тему для поиска на Википедии:')

    # Устанавливаем состояние пользователя в "ожидание темы для поиска на Википедии"
    bot.register_next_step_handler(message, search_wikipedia)


# Функция поиска на Википедии
def search_wikipedia(message):
    # Ищем статью на Википедии
    try:
        wikipedia.set_lang('ru')  # Устанавливаем язык поиска
        page = wikipedia.page(message.text)

        # Отправляем сообщение с заголовком статьи и первым абзацем
        bot.send_message(message.chat.id, f'page.titlepage.content.split(".")[0]')
    except wikipedia.exceptions.DisambiguationError as e:
        # Если найдено несколько статей, отправляем сообщение со списком возможных вариантов
        bot.send_message(message.chat.id, f'Найдено несколько возможных статей: ", ".join(e.options)')
    except wikipedia.exceptions.PageError:
        # Если статья не найдена, отправляем сообщение об ошибке
        bot.send_message(message.chat.id, 'Статья не найдена.')

# Запускаем бота

bot.polling()