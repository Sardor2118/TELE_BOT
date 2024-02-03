import telebot

# Создаем экземпляр бота с токеном
bot = telebot.TeleBot('TOKEN')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который поможет вам. Чем могу помочь?")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Справочная информация: ...")

# Запускаем бота
bot.infinity_polling()
