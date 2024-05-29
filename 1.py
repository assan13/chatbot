import telebot
import random

# Вставьте ваш токен Telegram API
TOKEN = '7477213854:AAHXaL-jNYX-co1WIusrlA-b98JcrfM4ajE'

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения пар пользователей
user_pairs = {}

# Функция для остановки диалога
def stop_chat(chat_id):
    if chat_id in user_pairs:
        pair_id = user_pairs[chat_id]
        if pair_id is not None:
            user_pairs.pop(chat_id)
            user_pairs.pop(pair_id)
            bot.send_message(pair_id, 'Диалог остановлен.')
            return True
    return False

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я чат-бот. Отправь /connect, чтобы начать чат.')

# Обработчик команды /connect
@bot.message_handler(commands=['connect'])
def connect(message):
    chat_id = message.chat.id

    # Проверка, есть ли уже пара для пользователя
    if chat_id in user_pairs:
        bot.reply_to(message, 'Вы уже находитесь в чате.')
    else:
        user_pairs[chat_id] = None
        bot.reply_to(message, 'Ожидайте собеседника...')

# Обработчик команды /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    chat_id = message.chat.id

    if stop_chat(chat_id):
        bot.reply_to(message, 'Диалог остановлен.')
    else:
        bot.reply_to(message, 'Вы не находитесь в чате.')

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def chat(message):
    chat_id = message.chat.id

    # Проверка, есть ли пара для пользователя
    if chat_id in user_pairs:
        pair_id = user_pairs[chat_id]

        # Если пользователь еще не имеет пару, сохраняем его ID
        if pair_id is None:
            for key, value in user_pairs.items():
                if value is None and key != chat_id:
                    user_pairs[key] = chat_id
                    user_pairs[chat_id] = key
                    bot.reply_to(message, 'Собеседник найден! Начинайте общение. Для выхода из диалога /stop')
                    bot.send_message(key, 'Собеседник найден! Начинайте общение. Для выхода из диалога /stop')
                    break
            if user_pairs[chat_id] is None:
                bot.reply_to(message, 'Поиск собеседника...')
        else:
            # Отправляем сообщение пользователю-паре
            bot.send_message(pair_id, message.text)
    else:
        bot.reply_to(message, 'Для начала чата отправьте команду /connect.')

# Обработчик мультимедийных сообщений
@bot.message_handler(content_types=['photo', 'audio', 'voice', 'video', 'document'])
def handle_media(message):
    chat_id = message.chat.id

    # Проверка, есть ли пара для пользователя
    if chat_id in user_pairs:
        pair_id = user_pairs[chat_id]

        # Если пользователь имеет пару, отправляем мультимедийное сообщение пользователю-паре
        if pair_id is not None:
            bot.forward_message(pair_id, chat_id, message.id)

# Запуск бота
bot.polling()