"""
Модуль с взаимодействием с бд
"""
import os
import pymysql


def get_connection():
    """
    Функция подключения к БД
    """
    connection = pymysql.connect(host='server102.hosting.reg.ru',
                                 user='u1450880_burym',
                                 password=os.getenv('PASS'),
                                 db='u1450880_burym')
    return connection


class DbAllin:
    """
    Класс содержит основные методы в боте.
    """

    @staticmethod
    def bd_user_add(client_info, chat_id):
        """
        Метод, добавляет юзера: "client_info", и его "chat_id" в бд.
        """
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                sql = 'INSERT INTO `users` (`client_info`, `chat_id`) VALUES (%s, %s)'
                cursor.execute(sql, (client_info, chat_id))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f'Ошибка при выполнении запроса: {e}')

    @staticmethod
    def check_chat_id_exists(chat_id):
        """
        Метод, проверяет, существует ли пользователь в БД.
        Если результат count-a больше 0, значит запись существует.
        """
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                sql = 'SELECT COUNT(*) FROM users WHERE chat_id = %s'
                cursor.execute(sql, (chat_id,))
                result = cursor.fetchone()
                if result[0] > 0:
                    return True
                else:
                    return False
        except pymysql.MySQLError as e:
            print(f'Ошибка при выполнении запроса: {e}')

    @staticmethod
    def bd_add_user_info(user_info, chat_id):
        """
        Метод, вставляет в таблицу БД "consulting_info" информацию в колонки
         `user_info`, `chat_id`
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'INSERT INTO `consulting_info` (`user_info`, `chat_id`) VALUES (%s, %s)'
                    cursor.execute(sql, (user_info, chat_id))
                    connection.commit()
        except Exception as e:
            print(f'Произошла ошибка: {e}')

    @staticmethod
    def bd_add_idea(client_info, chat_id):
        """
        Метод, вставляет в таблицу БД "consulting_info" информацию в колонку
         `ideainfo`. Это текст описание идеи татуировки.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'UPDATE consulting_info SET ideainfo = %s WHERE chat_id = %s'
                    cursor.execute(sql, (client_info, chat_id))
                    connection.commit()
        except Exception as e:
            print(f'Произошла ошибка: {e}')

    @staticmethod
    def bd_add_rostves(client_info, chat_id):
        """
        Метод, вставляет в таблицу БД "consulting_info" информацию в колонку
         `rostves`. Это текст описание основных параметров клиента.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'UPDATE consulting_info SET rostves = %s WHERE chat_id = %s'
                    cursor.execute(sql, (client_info, chat_id))
                    connection.commit()
        except Exception as e:
            print(f'Произошла ошибка: {e}')

    @staticmethod
    def bd_add_minus(client_info, chat_id):
        """
        Метод, вставляет в таблицу БД "consulting_info" информацию в колонку
         `minus`. Это текст описание противопоказаний клиента.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'UPDATE consulting_info SET minus = %s WHERE chat_id = %s'
                    cursor.execute(sql, (client_info, chat_id))
                    connection.commit()
        except Exception as e:
            print(f'Произошла ошибка: {e}')

    @staticmethod
    def bd_add_consultation_date(client_info, chat_id):
        """
        Метод, вставляет в таблицу БД "consulting_info" информацию в колонку
         `consultationdate`.Это текст описание желаемой даты сеанса тату.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'UPDATE consulting_info SET consultationdate = %s WHERE chat_id = %s'
                    cursor.execute(sql, (client_info, chat_id))
                    connection.commit()
        except Exception as e:
            print(f'Произошла ошибка: {e}')

    @staticmethod
    def bd_add_consa_inf(client_info, chat_id):
        """
        Метод, вставляет в таблицу БД "consulting_info" информацию в колонку
         `consa`. Это текст - может ли клиент приехать на консультацию.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'UPDATE consulting_info SET consa = %s WHERE chat_id = %s'
                    cursor.execute(sql, (client_info, chat_id))
                    connection.commit()
        except Exception as e:
            print(f'Произошла ошибка: {e}')

    @staticmethod
    def bd_foto_save(photo_id, chat_id):
        """
        Метод, вставляет в таблицу БД "consulting_info" информацию в колонку
        `foto_tattoo`. Это колонка хранит имена сохраненных фотографий.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'UPDATE consulting_info SET foto_tattoo = %s WHERE chat_id = %s'
                    photo_str = ', '.join(photo_id)
                    cursor.execute(sql, (photo_str, chat_id))
                    connection.commit()
        except Exception as e:
            print(f'Произошла ошибка: {e}')

    @staticmethod
    def bd_show_all():
        """
        Метод, отправляет информацию из таблицы БД "consulting_info" колонок
         'user_info' и 'chat_id'. Сохраняет их в список либо отправляет
         пустой список если информации нет.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'SELECT user_info, chat_id FROM consulting_info'
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    return results
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            return []

    @staticmethod
    def get_media_ref_bot(chat_id):
        """
        Метод, отправляет информацию из таблицы БД "consulting_info" из
        колоноки 'foto_tattoo'.
        Отправляет имена фотографий.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'SELECT foto_tattoo FROM consulting_info WHERE chat_id = %s'
                    cursor.execute(sql, (chat_id,))
                    result = cursor.fetchone()
                    if result and result[0]:
                        return result[0].split(', ')
                    else:
                        print('Нет сохраненных фотографий')
        except Exception as e:
            print(f'Произошла ошибка при извлечении из базы данных: {e}')

    @staticmethod
    def get_all_info(chat_id):
        """
        Метод, отправляет всю информацию из таблицы БД "consulting_info" по
        заданному значению колонки chat_id, на которой регистрировался
        пользователь.
        """
        try:
            connection = get_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = 'SELECT user_info, ideainfo, rostves, minus, consa, consultationdate FROM consulting_info WHERE chat_id = %s'
                    cursor.execute(sql, (chat_id,))
                    result = cursor.fetchone()
                    if result:
                        return {
                            'user_info': result[0],
                            'ideainfo': result[1],
                            'rostves': result[2],
                            'minus': result[3],
                            'consa': result[4],
                            'consultationdate': result[5]
                        }
                    else:
                        print('Нет данных для данного chat_id')
                        return None
        except Exception as e:
            print(f'Произошла ошибка при извлечении из базы данных: {e}')
            return None
