import telebot

# Вставьте сюда ваш токен, полученный от BotFather
TOKEN = '8734402843:AAGxZBOvJf9BnDewwTV_iFKvCL_lhJGx1JY'

# Создаём объект бота
bot = telebot.TeleBot(8734402843:AAGxZBOvJf9BnDewwTV_iFKvCL_lhJGx1JY)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я эхо-бот. Напиши что-нибудь, и я повторю.')

# Обработчик любых текстовых сообщений (не команд)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Отправляем обратно тот же текст, который прислал пользователь
    bot.reply_to(message, message.text)

# Запускаем бота (бесконечный опрос сервера Telegram)
bot.polling()