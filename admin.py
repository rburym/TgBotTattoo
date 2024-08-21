"""
Модуль с логикой работы действий админа/владельца тг бота.
"""
from keyboard import KeyboardAllin
from database import DbAllin
from telebot import types
from config import bot, ADMIN_ID

db = DbAllin()
kb = KeyboardAllin()


@bot.message_handler(commands=['admin'])
def admin_actions(message):
    """
    В этой функции бот сравнивает chat.id с значением ADMIN_ID, и либо здоровается с админом и кидает ему
    админовскую клавиатуру либо пишет что пользователь не админ.
    """
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        bot.send_message(chat_id, f'Включена клавиатура Админа.', reply_markup=kb.admin_kb())
    else:
        bot.send_message(chat_id, f'У вас нет прав админа.')


@bot.message_handler(func=lambda message: message.text == 'Клиенты')
def show_all_admin(message):
    """
    Действия бота при нажатии кнопки 'Клиенты'
    Обращается к бд, таблицы consulting_info и
    отправляет админу информацию по существующим клиентам.
    """
    try:
        chat_id = message.chat.id
        if chat_id == ADMIN_ID:
            load = db.bd_show_all()
            response_message = "Список пользователей:\n"
            if not load:
                response_message = "Нет доступных данных."
            else:
                for user_info in load:
                    response_message += f"|Айди: {user_info[1]}| Инфо:{user_info[0]}\n"
            try:
                bot.send_message(ADMIN_ID, response_message)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


@bot.message_handler(func=lambda message: message.text == 'Инфо')
def info_admin(message):
    """
    Когда админ нажимает кнопку с текстом "Информация", бот запрашивает
    айди, информация по которому будет отправлена.

    Args:
        message (telebot.types.Message):
        Сообщение, отправленное администратору.
    """
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        bot.send_message(ADMIN_ID, 'Введите Айди нужного вам пользователя: ')
        bot.register_next_step_handler(message, send_client_info_admin)
    else:
        print(f'Клиент не Админ, айди: {chat_id}')


def send_client_info_admin(message):
    """
    Обрабатывает отправленное сообщение. Ищет в БД consulting_info,
    столбца chat_id полученный айди. Отправляет информацию из всех столбцов
    таблицы. Отдельно отправляет фотографии получив их из колонки photo_ref.
    Разбиение на чанки, что бы в 1 сообщение не было больше 10 фотографий.
    """
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        sinfo = message.text
        client_info = db.get_all_info(sinfo)
        if client_info:
            response_message = (
                f"Информация о клиенте:\n"
                f"Пользователь: {client_info['user_info']}\n"
                f"{client_info['ideainfo']}\n"
                f"{client_info['rostves']}\n"
                f"{client_info['minus']}\n"
                f"Консультация: {client_info['consa']}\n"
                f"{client_info['consultationdate']}"
            )
            try:
                bot.send_message(ADMIN_ID, response_message)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        else:
            print(f"Нет информации для chat_id {sinfo}")
        bot.send_message(ADMIN_ID, 'Референсы тату клиента и место расположения:')
        tattoo_ref = db.get_media_ref_bot(message.text)
        chunk_size = 10
        for i in range(0, len(tattoo_ref), chunk_size):
            media_chunk1 = [types.InputMediaPhoto(media=admin_id) for admin_id in tattoo_ref[i:i + chunk_size]]
            bot.send_media_group(ADMIN_ID, media_chunk1)
    else:
        print(f'Клиент не Админ, айди: {chat_id}')


@bot.message_handler(func=lambda message: message.text == 'Назад?')
def admin_back(message):
    """
    Когда администратор нажимает кнопку с текстом "Назад?",
    бот возвращает в главное меню.
    """
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        bot.send_message(message.chat.id, f'Возвращение в главное меню', reply_markup=kb.user_kb())
    else:
        print(f'Клиент не Админ, айди: {chat_id}')
