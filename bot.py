"""
Модуль с логикой работы бота
"""

from config import ADMIN_ID, bot
from database import DbAllin
from keyboard import KeyboardAllin
from telebot import types

db = DbAllin()
kb = KeyboardAllin()
temp_data = {}
photo_ref = []


@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Функция приветствия, принимает команду 'start'. Cравнивает tg id
    пользователя с tg id в таблтце users базы данных. Если tg id пользователя
    есть в базе, то пользователю выдаётся клавиатура users_kb, иначе
    регестрирует клиента.
    """
    chat_id = message.chat.id
    if db.check_chat_id_exists(message.chat.id):
        print(f"Запись с chat_id {message.chat.id} существует.")
        bot.send_message(message.chat.id, f'Возвращение в главное меню',
                         reply_markup=kb.user_kb())
    else:
        print(f"Запись с chat_id {message.chat.id} не найдена.")
        bot.send_message(chat_id,
                         'Привет! Это бот для консультации перед сеансом! '
                         '\nДля продолжения работы, введите своё имя и укажи'
                         'те Ник в Телеграмме.\n Пример: Slim Shady, @tgusert'
                         'ag')
        temp_data[chat_id] = {}
        bot.register_next_step_handler(message, user_registry)


def user_registry(message):
    """
    Функция предлагает пользователю сохранить или изменить введенные для
    регистрации данные.
    """
    chat_id = message.chat.id
    data = message.text
    temp_data[chat_id]['client_info'] = data
    bot.send_message(chat_id, f'Проверьте правильность указанных вами данных:'
                              f' {data}.', reply_markup=kb.data_save_kb())


@bot.message_handler(func=lambda message: message.text == '⚫️Консультация 📣')
def button_consulting(message):
    """
    Действия бота при нажатии кнопки '⚫️Консультация 📣'
    Запускает процесс консультации
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Здравствуйте! Первый вопрос.',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(chat_id, f'Вам уже есть 18 лет ?',
                     reply_markup=kb.adulthood_kb())


@bot.callback_query_handler(func=lambda call: call.data == 'continue_consalting')
def continue_consalting_btn(call):
    """
    Функция отвечает за кнопку button_yes функции button_consulting,
    продолжает консультацию при условии что клиенту есть 18 лет.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=f'Отлично. Тогда, для начала. Текстом, в одном'
                               f' сообщении, опишите свою идею максимал'
                               f'ьно подробно.')
    photo_ref.clear()
    bot.register_next_step_handler(message, save_first_consulting_info)


@bot.callback_query_handler(func=lambda call: call.data == 'stop_consalting')
def stop_consalting_btn(call):
    """
    Функция отвечает за кнопку button_no функции button_consulting,
    останавливает консультацию при условии что клиенту нет 18 лет.
    Возвращает к главной клавиатуре user_kb.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=f'Извините, но мы не можем продолжить консульт'
                               f'ацию.')
    bot.send_message(message.chat.id, f'Буду ждать вас на сеанс после соверше'
                                      f'ннолетия)', reply_markup=kb.user_kb())


def save_first_consulting_info(message):
    """
    Функция сохраняет в таблицу consulting_info
    описание идеи которую передает клиент.
    """
    chat_id = message.chat.id
    db.bd_add_idea('Описание идеи: ' + message.text, chat_id)
    bot.send_message(message.chat.id, f'Теперь, прикрепите примеры работ, кот'
    f'орые вам понравились. Работа не обязательно должна на 100% совпадать с '
    f'идеей (например: вы хотите розу, а на работе изображена лилия). Фото ну'
    f'жны, чтобы лучше понять ваши вкусы, и было проще разработать эскиз по в'
    f'ашему запросу. Отправьте только фотографии, без текста. После отправки '
    f'фотографий, нажмите кнопку "Готово".',
                     reply_markup=kb.next_step_handler1())
    bot.register_next_step_handler(message, handle_photos_1)


@bot.message_handler(content_types=['photo'])
def handle_photos_1(message):
    """
    Функция сохраняет фотографии, а их имена
    сохраняет в photo_ref = [].
    """
    chat_id = message.chat.id
    fileid = message.photo[-1].file_id
    if fileid not in photo_ref:
        file_info = bot.get_file(fileid)
        downloaded_file = bot.download_file(file_info.file_path)
        folder_path = 'photos/'
        file_name = f"{chat_id}_{fileid}.jpg"
        file_path = folder_path + file_name
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        photo_ref.append(fileid)


@bot.message_handler(func=lambda message: message.text == 'Готово')
def button_done1(message):
    """
    При нажатии кнопки 'Готово' продолжает консультацию,
    отправляет сообщение клиенту.
    """
    bot.send_message(message.chat.id, f'Далее. Пришлите фото, на каком месте '
    f'будет тату. Нужна фотография этого места, чтобы я могла оценить количес'
    f'тво родинок, наличие шрамов/растяжек и других татуировок.',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, handle_photos_2)


@bot.message_handler(content_types=['photo'])
def handle_photos_2(message):
    """
    Функция сохраняет (скачивает) фотографии,
    а их имена отправляет в photo_ref = [].
    """
    chat_id = message.chat.id
    fileid = message.photo[-1].file_id
    if fileid not in photo_ref:
        file_info = bot.get_file(fileid)
        downloaded_file = bot.download_file(file_info.file_path)
        folder_path = 'photos/'
        file_name = f"{chat_id}_{fileid}.jpg"
        file_path = folder_path + file_name
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        photo_ref.append(fileid)
    bot.send_message(message.chat.id, f'Данные приняты.')
    bot.send_message(message.chat.id, f'Укажите свои параметры (можно примерн'
                                      f'о), напишите свой рост/вес')
    bot.register_next_step_handler(message, save_second_consulting_info)


def save_second_consulting_info(message):
    """
    Функция сохраняет информацию присланную
    клиентом в бд в таблицу consulting_info.
    """
    db.bd_add_rostves('Параметры клиента: ' + message.text, message.chat.id)
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Есть ли у вас противопоказания?',
                     reply_markup=kb.contraindications_kb())


@bot.callback_query_handler(func=lambda call: call.data == 'contraindications_continue')
def contraindications_continue_btn(call):
    """
    Функция отвечает за кнопку contraindications_continue функции
    save_third_consulting_info, продолжает консультацию при условии что у
    клиента нет противопоказаний. Отправляет в бд в таблицу consulting_info
    сообщение о наличие противопоказаний.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=f'Отлично, противопоказаний нет.')
    db.bd_add_minus('Противопоказаний нет', chat_id)
    bot.send_message(chat_id, f'Укажите, можете ли вы при необходимости приех'
                              f'ать на бесплатную очную консультацию? ',
                     reply_markup=kb.come_consulting_kb())


@bot.callback_query_handler(func=lambda call: call.data == 'contraindications_stop')
def contraindications_continue_two(call):
    """
    Функция отвечает за кнопку contraindications_stop функции
    save_third_consulting_info, при условии что у клиента есть
    противопоказания, просит клиента о них написать.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=f'Отправьте одним сообщением, (текстом - это '
                               f'важно) о том, какие у вас противопоказания')
    bot.register_next_step_handler(message, save_third_consulting_info)


def save_third_consulting_info(message):
    """
    Функция сохраняет сообщение о противопоказаниях
    и отправляет информацию о них в бд в таблицу consulting_info.
    """
    db.bd_add_minus('Есть противопоказания: ' + message.text, message.chat.id)
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Укажите, можете ли вы при необходимости '
                              f'приехать на бесплатную очную консультацию? ',
                     reply_markup=kb.come_consulting_kb())


@bot.callback_query_handler(func=lambda call: call.data == 'button_one')
def consalting_btn_one(call):
    """
    Функция отвечает за кнопку button_one функции save_fourth_consulting_info,
    сохраняет данные в бд таблицу consulting_info о выбранной кнопке.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=f'Записан ответ > Могу приехать')
    bot.send_message(chat_id, f'Вам удобнее провести сеанс в будни или выходн'
    f'ые? Можете указать примерные даты, когда планировали сделать '
                              f'татуировку.')
    db.bd_add_consa_inf('>Могу приехать на консультацию', chat_id)
    bot.register_next_step_handler(message, save_fourth_consulting_info)


@bot.callback_query_handler(func=lambda call: call.data == 'button_two')
def consalting_btn_two(call):
    """
    Функция отвечает за кнопку button_two функции save_fourth_consulting_info,
    сохраняет данные в бд таблицу consulting_info о выбранной кнопке.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=f'Записан ответ > Не могу приехать')
    bot.send_message(chat_id, f'Вам удобнее провести сеанс в будни или выходн'
    f'ые? Можете указать примерные даты, когда планировали сделать татуировк'
                              f'у.')
    db.bd_add_consa_inf('>Не могу приехать на консультацию', chat_id)
    bot.register_next_step_handler(message, save_fourth_consulting_info)


@bot.callback_query_handler(func=lambda call: call.data == 'button_three')
def consalting_btn_three(call):
    """
    Функция отвечает за кнопку button_three функции
    save_fourth_consulting_info, сохраняет данные в бд таблицу consulting_info
    о выбранной кнопке.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=f'Записан ответ > Не из Москвы.')
    bot.send_message(chat_id, f'Вам удобнее провести сеанс в будни или выходн'
    f'ые? Можете указать примерные даты, когда планировали сделать татуировку'
                              f'.')
    db.bd_add_consa_inf('>Клиент не из Москвы', chat_id)
    bot.register_next_step_handler(message, save_fourth_consulting_info)


def save_fourth_consulting_info(message):
    """
    Функция сохраняет информацию клиента о дате и имена фотографий в бд
    таблицу consulting_info. В колонки foto_info и consultingdate. А также
    оповещает ADMIN_ID о новой записи.
    """
    chat_id = message.chat.id
    db.bd_add_consultation_date('Уазанная дата:' + message.text, chat_id)
    if not photo_ref:
        print('Нет сохраненных фотографий')
        return
    db.bd_foto_save(photo_ref, chat_id)
    bot.send_message(ADMIN_ID, f'Появилась новая запись! '
                               f'Новый айди: |{chat_id}|')
    bot.send_message(chat_id, f' Спасибо! Я свяжусь с вами в ближайшее время '
                              f'и сориентирую по стоимости и ближайшим датам.'
                     , reply_markup=kb.user_kb())


@bot.message_handler(func=lambda message: message.text == '⚪️Информация клиенту 📝')
def button_info(message):
    """
    Действия бота при нажатии кнопки '⚪️Информация клиенту 📝'
    Дает доступ к двум кнопка 🟡Важно до сеанса до сеанса и 🟢Уход после сеанса.
    """
    bot.send_message(message.chat.id, f'Информация клиенту',
                     reply_markup=kb.info_kb())


@bot.message_handler(func=lambda message: message.text == '🟡Важно до сеанса')
def button_beforett(message):
    """
    Действия бота при нажатии кнопки '🟡Важно до сеанса'
    Дает доступ к 4 кнопкам 🟡Подготовка, 🟡Противопоказания,
    🟡Как выбрать дату, 🟡Назад.
    """
    bot.send_message(message.chat.id, f'До сеанса',
                     reply_markup=kb.important_kb())


@bot.message_handler(func=lambda message: message.text == '🟢Уход после сеанса')
def button_aftertt(message):
    """
    Действия бота при нажатии кнопки '🟢Уход после сеанса'
    Дает доступ к трем кнопкам: 🟢Пленки, 🟢Пеленки, 🟢Назад.
    """
    bot.send_message(message.chat.id, f'Уход после сеанса',
                     reply_markup=kb.recover_kb())


@bot.message_handler(func=lambda message: message.text == '🟡Назад')
def button_back(message):
    """
    Действия бота при нажатии кнопки '🟡Назад'
    Возвращает назад в меню между 🟢Уход после сеанса и 🟡Важно до сеанса.
    """
    bot.send_message(message.chat.id, f'Назад', reply_markup=kb.info_kb())


@bot.message_handler(func=lambda message: message.text == 'Назад')
def button_back(message):
    """
    Действия бота при нажатии кнопки 'Назад'.
    Возвращает в предыдущее меню между
    ️⚪️Информация клиенту 📝 и ⚫️Консультация 📣.
    """
    bot.send_message(message.chat.id, f'Главное меню',
                     reply_markup=kb.user_kb())


@bot.message_handler(func=lambda message: message.text == '🟢Назад')
def button_back(message):
    """
    Действия бота при нажатии кнопки '🟢Назад'
    Возвращает назад в меню между 🟢Уход после сеанса и 🟡Важно до сеанса.
    """
    bot.send_message(message.chat.id, f'Главное меню',
                     reply_markup=kb.info_kb())


@bot.callback_query_handler(func=lambda call: call.data == 'save_data')
def save_btn(call):
    """
    Функция отвечает за кнопку button_save, функции save_entry. Сохранить
    данные введенные пользователем в бд, сохраняет введенное
    сообщение и chat_id. Сохраняет данные в таблицы users и consulting_info.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    db.bd_user_add(temp_data[chat_id]['client_info'], chat_id)
    db.bd_add_user_info(temp_data[chat_id]['client_info'], chat_id)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Данные сохранены.')
    bot.send_message(message.chat.id, f'Теперь вы можете пользоваться ботом!',
                     reply_markup=kb.user_kb())


@bot.callback_query_handler(func=lambda call: call.data == 'change_data')
def change_btn(call):
    """
    Функция отвечает за кнопку button_change в функции save_entry, изменение
    данных введеных пользователем, возвращает клиента в функцию welcome,
    заново регистрирует.
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Изменение данных. Необходимо заново пройти ре'
                               'гистрацию.')
    welcome(message)
