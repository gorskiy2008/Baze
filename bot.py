import telebot
import requests
import os
import tempfile

# Вставьте ваш НОВЫЙ токен (старый нужно отозвать у BotFather)
TOKEN = '8734402843:AAGxZBOvJf9BnDewwTV_iFKvCL_lhJGx1JY'
bot = telebot.TeleBot("8734402843:AAGxZBOvJf9BnDewwTV_iFKvCL_lhJGx1JY")

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я умею отправлять фото, видео и голосовые.\n'
                          'Используй команды:\n'
                          '/photo – получить фото\n'
                          '/video – получить видео\n'
                          '/voice – получить голосовое сообщение\n'
                          'А ещё ты можешь просто прислать мне фото, видео или голосовое, и я их сохраню!')

# Команда /photo – отправляем фото
@bot.message_handler(commands=['photo'])
def send_photo(message):
    try:
        # Сначала пробуем отправить локальный файл
        with open('cat.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption='Вот тебе фото котика!')
    except FileNotFoundError:
        # Если файла нет, скачиваем изображение по URL и отправляем
        try:
            url = 'https://cataas.com/cat'
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Сохраняем во временный файл
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                    tmp.write(response.content)
                    tmp_path = tmp.name
                
                # Отправляем из временного файла
                with open(tmp_path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption='А вот котик из интернета')
                
                # Удаляем временный файл
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
        # Отправляем видео по URL
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
        # Отправляем голосовое из локального файла
        with open('sample.ogg', 'rb') as voice:
            bot.send_voice(message.chat.id, voice, caption='Голосовое сообщение')
    except FileNotFoundError:
        # Если файла нет, используем пример из интернета (нужен прямой URL на .ogg файл)
        bot.reply_to(message, 'Положите файл sample.ogg в папку с ботом')
        # Альтернатива: можно отправить голосовое, сгенерировав текст в речь через сторонний API

# Обработчик полученных фото от пользователя
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Получаем ID фото (самое большое разрешение)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    
    # Скачиваем фото
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Сохраняем на диск
    with open(f'photo_{message.from_user.id}_{message.message_id}.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.reply_to(message, f'Фото получено и сохранено! Размер: {len(downloaded_file)} байт')

# Обработчик полученных видео от пользователя
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open(f'video_{message.from_user.id}_{message.message_id}.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.reply_to(message, f'Видео получено! Длительность: {message.video.duration} сек')

# Обработчик полученных голосовых от пользователя
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open(f'voice_{message.from_user.id}_{message.message_id}.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.reply_to(message, f'Голосовое получено! Длительность: {message.voice.duration} сек')

# Обработчик всех остальных сообщений (эхо)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск бота
print("Бот запущен...")
bot.polling()