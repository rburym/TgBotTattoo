"""
Модуль содержит клавиатуры, используемые в телеграм-боте.
"""

import telebot
from telebot import types


class KeyboardAllin:
    """
    Класс содержит основные клавиатуры, используемые в боте.
    """

    @staticmethod
    def data_save_kb() -> types.InlineKeyboardMarkup:
        """
        Предлагает сохранить или изменить данные, регастрация пользователя

        Returns:
            types.InlineKeyboardMarkup: Клавиатура с 2 кнопками
        """
        keyboard = telebot.types.InlineKeyboardMarkup()
        button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
                                                         callback_data='save_data')
        button_change = telebot.types.InlineKeyboardButton(text="Изменить",
                                                           callback_data='change_data')
        keyboard.add(button_save, button_change)
        return keyboard

    @staticmethod
    def user_kb() -> types.ReplyKeyboardMarkup:
        """
        Создает основную клавиатуру юзера, Информация и Консультация.

        Returns:
            types.ReplyKeyboardMarkup: Клавиатура с 2 кнопками
        """
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('⚪️Информация клиенту 📝')
        btn2 = types.KeyboardButton('⚫️Консультация 📣')
        kb.row(btn1, btn2)
        return kb

    @staticmethod
    def info_kb() -> types.ReplyKeyboardMarkup:
        """
        После нажатия '⚪️Информация клиенту 📝' создает/открывает новую клавиатуру с 3 кнопками.

        Returns:
            types.ReplyKeyboardMarkup: Клавиатура с 3 кнопками
        """
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🟡Важно до сеанса')
        btn2 = types.KeyboardButton('Назад')
        btn3 = types.KeyboardButton('🟢Уход после сеанса')
        kb.row(btn1, btn3)
        kb.row(btn2)
        return kb

    @staticmethod
    def important_kb() -> types.ReplyKeyboardMarkup:
        """
        После нажатия клавиатуры "🟡Важно до сеанса" создает новую клавиатуру с 4 кнопками.

        Returns:
            types.ReplyKeyboardMarkup: Клавиатура с 4 кнопками
        """
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🟡Подготовка')
        btn2 = types.KeyboardButton('🟡Противопоказания')
        btn3 = types.KeyboardButton('🟡Как выбрать дату')
        btn4 = types.KeyboardButton('🟡Назад')
        kb.row(btn1, btn2)
        kb.row(btn3, btn4)
        return kb

    @staticmethod
    def next_step_handler1() -> types.ReplyKeyboardMarkup:
        """
        Создает клавиатуру с 1 кнопкой.

        Returns:
            types.ReplyKeyboardMarkup: Клавиатура с 1 кнопкой
        """
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Готово')
        kb.row(btn1)
        return kb

    @staticmethod
    def recover_kb() -> types.ReplyKeyboardMarkup:
        """
        После нажатия "🟢Уход после сеанса" создает новую клавиатуру с 3 кнопками.

        Returns:
            types.ReplyKeyboardMarkup: Клавиатура с 3 кнопками
        """
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🟢Пленки')
        btn2 = types.KeyboardButton('🟢Пеленки')
        btn3 = types.KeyboardButton('🟢Назад')
        kb.row(btn1, btn2)
        kb.row(btn3)
        return kb

    @staticmethod
    def adulthood_kb() -> types.InlineKeyboardMarkup:
        """
        Создает две кнопки на вопрос о том, есть ли 18 лет

        Returns:
            types.InlineKeyboardMarkup: 2 кнопки
        """
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        button_yes = telebot.types.InlineKeyboardButton(text="Да",
                                                        callback_data='continue_consalting')
        button_no = telebot.types.InlineKeyboardButton(text="Нет",
                                                       callback_data='stop_consalting')
        keyboard1.add(button_yes, button_no)
        return keyboard1

    @staticmethod
    def contraindications_kb() -> types.InlineKeyboardMarkup:
        """
        Создает клавиатуру по противопоказаниям

        Returns:
            types.InlineKeyboardMarkup: 2 кнопки
        """
        keyboard2 = telebot.types.InlineKeyboardMarkup()
        button_no = telebot.types.InlineKeyboardButton(text="Нет.",
                                                       callback_data='contraindications_continue')
        button_yes = telebot.types.InlineKeyboardButton(text="Есть.",
                                                        callback_data='contraindications_stop')
        keyboard2.add(button_no, button_yes)
        return keyboard2

    @staticmethod
    def come_consulting_kb() -> types.InlineKeyboardMarkup:
        """
        Создает кнопки на вопрос, сможет ли клиент приехать на консультацию

        Returns:
            types.InlineKeyboardMarkup: Клавиатура с 3 кнопками
        """
        keyboard3 = telebot.types.InlineKeyboardMarkup()
        button_one = telebot.types.InlineKeyboardButton(text="Могу",
                                                        callback_data='button_one')
        button_two = telebot.types.InlineKeyboardButton(text="Не могу",
                                                        callback_data='button_two')
        button_three = telebot.types.InlineKeyboardButton(text="Не из Москвы",
                                                          callback_data='button_three')
        keyboard3.add(button_one, button_two, button_three)
        return keyboard3

    @staticmethod
    def admin_kb() -> types.ReplyKeyboardMarkup:
        """
        Создает клавиатуру администратора.

        Returns:
            types.ReplyKeyboardMarkup: Клавиатура с 3 кнопками
        """
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Клиенты')
        btn2 = types.KeyboardButton('Инфо')
        btn3 = types.KeyboardButton('Назад?')
        kb.row(btn1, btn2)
        kb.row(btn3)
        return kb
