"""
Модуль запуска бота.
"""
from bot import bot

if __name__ == '__main__':
    print('Бот запущен!')
    from admin import bot
    bot.infinity_polling()
