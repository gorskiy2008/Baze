import telebot

# Вставьте ваш токен
TOKEN = '8734402843:AAGxZBOvJf9BnDewwTV_iFKvCL_lhJGx1JY'

bot = telebot.TeleBot("8734402843:AAGxZBOvJf9BnDewwTV_iFKvCL_lhJGx1JY")

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я умею отправлять фото и видео.\n'
                          'Используй команды:\n'
                          '/photo – получить фото\n'
                          '/video – получить видео')

# Команда /photo – отправляем фото
@bot.message_handler(commands=['photo'])
def send_photo(message):
    # Способ 1: Отправить фото из файла на компьютере
    # Убедитесь, что файл 'cat.jpg' лежит в той же папке, что и скрипт
    try:
        with open('cat.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption='Вот тебе фото котика!')
    except FileNotFoundError:
        # Если файла нет, отправим фото по URL
        url = 'https://cataas.com/cat'  # сервис случайных котиков
        bot.send_photo(message.chat.id, url, caption='А вот котик из интернета')

# Команда /video – отправляем видео
@bot.message_handler(commands=['video'])
def send_video(message):
    # Способ 1: Отправить видео из локального файла
    try:
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption='Вот видео', supports_streaming=True)
    except FileNotFoundError:
        # Если файла нет, используем видео по ссылке (пример)
        video_url = 'http://techslides.com/demos/sample-videos/small.mp4'
        bot.send_video(message.chat.id, video_url, caption='Пример видео из интернета')

# Обработчик всех остальных сообщений (эхо)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск бота
bot.polling()