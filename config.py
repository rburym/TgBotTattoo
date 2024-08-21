"""
Модуль для настройки Telegram-бота.
"""
import os
import telebot

TOKEN = os.getenv('TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
bot = telebot.TeleBot(TOKEN)
