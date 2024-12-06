import telebot # библиотека telebot
from config import token # импорт токена
import re

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user_command(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            try:
                bot.ban_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
            except telebot.apihelper.ApiException as e:
                bot.reply_to(message, f"Ошибка бана: {e}")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if re.search(r"https?:\/\/\S+", message.text):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Администраторы не могут быть забанены.")
        else:
            try:
                bot.ban_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь @{message.from_user.username} забанен за спам.")
            except telebot.apihelper.ApiException as e:
                bot.reply_to(message, f"Ошибка бана: {e}")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)
    
bot.polling()