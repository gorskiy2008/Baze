import telebot
import requests
import os
import tempfile

# ВСТАВЬТЕ СЮДА НОВЫЙ ТОКЕН (старый нужно отозвать у BotFather)
TOKEN = '8734402843:AAGxZBOvJf9BnDewwTV_iFKvCL_lhJGx1JY'
bot = telebot.TeleBot("8734402843:AAGxZBOvJf9BnDewwTV_iFKvCL_lhJGx1JY")  # используем переменную, а не строку напрямую

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я умею отправлять фото, видео, голосовые и стикеры.\n'
                          'Используй команды:\n'
                          '/photo – получить фото\n'
                          '/video – получить видео\n'
                          '/voice – получить голосовое\n'
                          '/sticker – получить стикер\n'
                          'А ещё ты можешь прислать мне любое медиа (фото, видео, голос, стикер), и я его сохраню и покажу file_id.')

# Команда /photo – отправляем фото
@bot.message_handler(commands=['photo'])
def send_photo(message):
    try:
        with open('cat.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption='Вот тебе фото котика!')
    except FileNotFoundError:
        try:
            url = 'https://cataas.com/cat'
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                    tmp.write(response.content)
                    tmp_path = tmp.name
                with open(tmp_path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption='А вот котик из интернета')
                os.unlink(tmp_path)
            else:
                bot.reply_to(message, 'Не удалось загрузить фото :(')
        except Exception as e:
            bot.reply_to(message, f'Ошибка при загрузке фото: {e}')

# Команда /video – отправляем видео
@bot.message_handler(commands=['video'])
def send_video(message):
    try:
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption='Вот видео', 
                          supports_streaming=True, timeout=30)
    except FileNotFoundError:
        try:
            video_url = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
            bot.send_video(message.chat.id, video_url, caption='Пример видео из интернета',
                          supports_streaming=True)
        except Exception as e:
            bot.reply_to(message, f'Ошибка при загрузке видео: {e}')

# Команда /voice – отправляем голосовое
@bot.message_handler(commands=['voice'])
def send_voice(message):
    try:
        with open('sample.ogg', 'rb') as voice:
            bot.send_voice(message.chat.id, voice, caption='Голосовое сообщение')
    except FileNotFoundError:
        bot.reply_to(message, 'Положите файл sample.ogg в папку с ботом')

# Команда /sticker – отправляем стикер
@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    # Пример file_id стикера (из популярного набора "Sticker by Anna")
    # Вы можете заменить на свой, отправив боту любой стикер и скопировав file_id из ответа
    sticker_file_id = 'CAACAgIAAxkBAAEBuGpfyT6Z1jK7y8Q4Xq9z0JQr0H9uAAKAAQACFkJrAANDmQABZwABy4EAAQ0E'  # замените на реальный file_id
    try:
        bot.send_sticker(message.chat.id, sticker_file_id)
    except Exception as e:
        # Если file_id нерабочий, отправляем тестовый стикер из Telegram
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBuHBfyT7A5QABG95iW5iY5Q8X8Z8jAAKCAQACFkJrAAP2YzN5W5YAAQQBAAMCAQe1AAMGBA')
        bot.reply_to(message, f'Отправлен тестовый стикер. Ошибка с вашим file_id: {e}')

# Обработчик полученных фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'photo_{message.from_user.id}_{message.message_id}.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, f'Фото получено и сохранено! file_id: {file_id}')

# Обработчик полученных видео
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'video_{message.from_user.id}_{message.message_id}.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, f'Видео получено! file_id: {file_id}, длительность: {message.video.duration} сек')

# Обработчик полученных голосовых
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'voice_{message.from_user.id}_{message.message_id}.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, f'Голосовое получено! file_id: {file_id}, длительность: {message.voice.duration} сек')

# Обработчик полученных стикеров
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    file_id = message.sticker.file_id
    # Стикеры можно скачивать, но они в формате .webp
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'sticker_{message.from_user.id}_{message.message_id}.webp', 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, f'Стикер получен! file_id: {file_id} (сохранён как .webp)')

# Обработчик всех остальных сообщений (эхо)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск бота
print("Бот запущен...")
bot.polling()