import sqlite3
import datetime

from utils.settings_loader import DB_PATH
from utils.log_worker import Logger


class DBWorker:

    def execute(query: str, parameters: tuple[str | int]):
        """Выполнение SQL запроса

        Args:
            query (str): запрос

        Raises:
            ex: Исключение, сгенерированное запросом

        Returns:
            data (list | None): Данные, полученные запросом (None при отсутствии)
        """
        try:
            con = sqlite3.connect(DB_PATH)
            cursor = con.cursor()
            cursor.execute(query, parameters)
            con.commit()
            data = cursor.fetchall()
            if bool(data) != True:
                data = None
            return data
        except Exception as ex:
            Logger.error(ex)
            raise ex


    class Users:

        def add(telegram_id: int):
            """Добавление юзера

            Args:
                telegram_id (int): Telegram ID юзера
            """
            DBWorker.execute("INSERT INTO users (telegram_id, ban_state) VALUES (?, ?)", (telegram_id, 0))
        
        def get_by_tg_id(telegram_id: int):
            """Получение ID юзера по Telegram ID

            Args:
                telegram_id (int): Telegram ID юзера

            Returns:
                db_id (int | None): ID юзера
            """
            data = DBWorker.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id, ))
            if bool(data):
                return int(data[0][0])
            else:
                return data
        
        def get_by_db_id(db_id: str):
            """Получение Telegram ID юзера по ID

            Args:
                db_id (str): ID юзера

            Returns:
                telegram_id (int | None): Telegram ID юзера
            """
            data = DBWorker.execute("SELECT telegram_id FROM users WHERE id = ?", (db_id, ))
            if bool(data):
                return int(data[0][0])
            else:
                return data
        
        def get_ban_state(telegram_id: int):
            """Получение информации о бане юзера

            Args:
                telegram_id (int): Telegram ID юзера

            Returns:
                ban_state (bool | None): Состояние бана (True - забанен, False - нет)
            """
            data = DBWorker.execute("SELECT ban_state FROM users WHERE telegram_id = ?", (telegram_id, ))
            if bool(data):
                if data[0][0] == 0:
                    return False
                else:
                    return True
            else:
                return data
        
        def edit_ban_state(telegram_id: int, ban_state: bool):
            """Изменение значение бана для юзера

            Args:
                telegram_id (int): Telegram ID юзера
                ban_state (bool): Значение бана (True - забанить, False - разбанить)
            """
            if ban_state == True:
                ban = 1
            else:
                ban = 0
            DBWorker.execute("UPDATE users SET ban_state = ? WHERE telegram_id = ?", (ban, telegram_id))
        
        def get_all():
            """Получение списка всех юзеров

            Returns:
                user_list (list | None): Список юзеров
            """
            data = DBWorker.execute("SELECT * FROM users", ())
            return data


    class Admins:

        def add(telegram_id: int, nickname: str):
            """Добавление админа

            Args:
                telegram_id (int): Telegram ID админа
                nickname (str): Ник админа для идентефикации
            """
            DBWorker.execute("INSERT INTO admins (telegram_id, nickname) VALUES (?, ?)", (telegram_id, nickname))
        
        def get_all():
            """Получение всех админов бота

            Returns:
                admin_list (list | None): Список админов
            """
            data = DBWorker.execute("SELECT * FROM admins", ())
            return data
        
        def get_nick(telegram_id: int):
            """Получение ника админа

            Args:
                telegram_id (int): Telegram ID админа

            Returns:
                nickname (str | None): Ник админа
            """
            data = DBWorker.execute("SELECT nickname FROM admins WHERE telegram_id = ?", (telegram_id, ))
            if bool(data):
                return str(data[0][0])
            else:
                return data
        
        def get_by_tg_id(telegram_id: int):
            """Получение ID по Telegram ID

            Args:
                telegram_id (int): Telegram ID админа

            Returns:
                admin_db_id (int | None): ID админа
            """
            data = DBWorker.execute("SELECT id FROM admins WHERE telegram_id = ?", (telegram_id, ))
            if bool(data):
                return int(data[0][0])
            else:
                return data
        
        def get_by_db_id(admin_db_id: int):
            """Получение Telegram ID по ID

            Args:
                admin_db_id (int): ID админа

            Returns:
                admin_tg_id (int | None): Telegram ID админа
            """
            data = DBWorker.execute("SELECT telegram_id FROM admins WHERE id = ?", (admin_db_id, ))
            if bool(data):
                return int(data[0][0])
            else:
                return data
        
        def delete(telegram_id: int):
            """Удалить админа

            Args:
                telegram_id (int): Telegram ID админа
            """
            DBWorker.execute("DELETE FROM admins WHERE telegram_id = ?", (telegram_id, ))

    class MsgTemplates:
        """Пояснение к типам сообщений:
        welcome - приветственное сообщение, help - сообщение справки, 
        post - подпись к посту, ban - сообщение бана
        """

        def get(msg_type: str):
            """Получение шаблона сообщения

            Args:
                msg_type (str): Тип сообщения

            Returns:
                msg_text (str | None): Текст сообщения
            """
            data = DBWorker.execute("SELECT msg_text FROM msg_templates WHERE msg_type = ?", (msg_type, ))
            if bool(data):
                return str(data[0][0])
            else:
                return data
        
        def edit(msg_type: str, msg_text: str):
            """Изменения шаблона сообщения

            Args:
                msg_type (str): Тип сообщения
                msg_text (str): Текст сообщения
            """
            DBWorker.execute("UPDATE msg_templates SET msg_text = ? WHERE msg_type = ?", (msg_text, msg_type))
    

    class Posts:

        def add(telegram_id: int, post_text: str | None):
            """Добавление поста в БД

            Args:
                telegram_id (int): Telegram ID предложившего запись юзера
                post_text (str | None): Текст поста (None при отсутствии)

            Returns:
                post_id (int): ID поста
            """
            user_db_id = DBWorker.Users.get_by_tg_id(telegram_id)
            if post_text == None:
                DBWorker.execute("INSERT INTO posts (user_id, state) VALUES (?, ?)", (user_db_id, 'editing'))
            else:
                DBWorker.execute("INSERT INTO posts (user_id, post_text, state) VALUES (?, ?, ?)", (user_db_id, post_text, 'editing'))
            data = DBWorker.execute("SELECT id FROM posts WHERE id = (SELECT MAX(id) FROM posts)", ())
            return int(data[0][0])

        def get(post_id: int):
            """Получение информации о посте по ID

            Args:
                post_id (int): ID поста

            Returns:
                post_data (list | None): Данные о посте (None при отсутствии)
            """
            data = DBWorker.execute("SELECT * FROM posts WHERE id = ?", (post_id, ))
            if bool(data):
                return data[0]
            else:
                return None
        
        def update(post_id: int, post_text: str | None):
            """Обновляет предложенного текст поста

            Args:
                post_id (int): ID поста
            """
            DBWorker.execute("UPDATE posts SET post_text = ? WHERE id = ?", (post_id, post_text))

        def suggest(post_id: int):
            """Принять пост в обработку

            Args:
                post_id (int): ID поста
            """
            DBWorker.execute("UPDATE posts SET state = 'suggested' WHERE id = ?", (post_id, ))
        
        def accept(post_id: int, send_date: datetime.datetime, disable_notification: bool):
            """Отправить пост в отложенную отправку

            Args:
                post_id (int): ID поста
                send_date (datetime.datetime): Время отправления
                disable_notification (bool): Отключить уведомление о посте
            """
            send_time = send_date.strftime("%d-%m-%Y %H:%M")
            DBWorker.execute("UPDATE posts SET send_date = ?, state = 'accept', disable_notification = ? WHERE id = ?", (send_time, disable_notification, post_id))

        def delete(post_id: int):
            """Удаление поста из БД

            Args:
                post_id (int): ID поста
            """
            DBWorker.execute("DELETE FROM posts WHERE id = ?", (post_id, ))
            DBWorker.PostFiles.delete(post_id)
    
        def get_all():
            """Получение всех постов

            Returns:
                data (list): Список постов
            """
            data = DBWorker.execute("SELECT * FROM posts", ())
            return data
        
        def get_with_timer():
            """Получение всех постов с установленным таймером

            Returns:
                post_list (list | None): Список постов
            """
            data = DBWorker.execute("SELECT * FROM posts WHERE state = 'accept'", ())
            return data
        
    
    class PostFiles:

        def add(post_id: int, file_id: str, file_type: str):
            """Добавление файлов поста в БД

            Args:
                post_id (int): ID поста
                file_id (str): ID файла в Telegram
                file_type (str): Тип файла (img - изображения, vid - видео, mus - музыка, doc - документ)
            """
            DBWorker.execute("INSERT INTO post_files (post_id, file_type, file_id) VALUES (?, ?, ?)", (post_id, file_type, file_id))
        
        def get(post_id: int):
            """Получение всех файлов для поста

            Args:
                post_id (int): ID поста

            Returns:
                files_list (list | None): список файлов
            """
            data = DBWorker.execute("SELECT * FROM post_files WHERE post_id = ?", (post_id, ))
            return data
        
        def delete(post_id: int):
            """Удаление файлов поста

            Args:
                post_id (int): ID поста
            """
            DBWorker.execute("DELETE FROM post_files WHERE post_id = ?", (post_id, ))
    

    class AdminPostStates:

        def add(post_id: int, admin_id: int, msg_id: int):
            """Добавление состояния поста для админов

            Args:
                post_id (int): ID поста
                admin_id (int): ID админа
                msg_id (int): ID сообщения с кнопками
            """
            DBWorker.execute("INSERT INTO admin_post_states (admin_id, post_id, msg_id) VALUES (?, ?, ?)", (admin_id, post_id, msg_id))
        
        def delete(post_id: int):
            """Удаление состояния поста

            Args:
                post_id (int): ID поста
            """
            DBWorker.execute("DELETE FROM admin_post_states WHERE post_id = ?", (post_id, ))
        
        def get_msg_id(post_id: int, admin_id: int):
            """Получение ID сообщения состояния поста

            Args:
                post_id (int): ID поста
                admin_id (int): ID админа

            Returns:
                msg_id (int | None): ID сообщения
            """
            data = DBWorker.execute("SELECT msg_id FROM admin_post_states WHERE post_id = ? AND admin_id = ?", (post_id, admin_id))
            if bool(data):
                return int(data[0][0])
            else:
                return None

    class Arts:

        def add(telegram_id: int, art_text: str | None):
            """Добавление арта в БД

            Args:
                telegram_id (int): Telegram ID предложившего арта юзера
                art_text (str | None): Текст арта (None при отсутствии)

            Returns:
                art_id (int): ID арта
            """
            user_db_id = DBWorker.Users.get_by_tg_id(telegram_id)
            if art_text == None:
                DBWorker.execute("INSERT INTO arts (user_id, state) VALUES (?, ?)", (user_db_id, 'editing'))
            else:
                DBWorker.execute("INSERT INTO arts (user_id, art_text, state) VALUES (?, ?, ?)", (user_db_id, art_text, 'editing'))
            data = DBWorker.execute("SELECT id FROM arts WHERE id = (SELECT MAX(id) FROM arts)", ())
            return int(data[0][0])

        def get(art_id: int):
            """Получение информации об арте по ID

            Args:
                art_id (int): ID арта

            Returns:
                art_data (list | None): Данные об арте (None при отсутствии)
            """
            data = DBWorker.execute("SELECT * FROM arts WHERE id = ?", (art_id, ))
            if bool(data):
                return data[0]
            else:
                return None
        
        def suggest(art_id: int):
            """Принять арт в обработку

            Args:
                post_id (int): ID арта
            """
            DBWorker.execute("UPDATE arts SET state = 'suggested' WHERE id = ?", (art_id, ))
        
        def accept(art_id: int, send_date: datetime.datetime):
            """Отправить арт в отложенную отправку

            Args:
                art_id (int): ID арта
                send_date (datetime.datetime): Время отправления
            """
            send_time = send_date.strftime("%d-%m-%Y %H:%M")
            DBWorker.execute("UPDATE arts SET send_date = ?, state = 'accept' WHERE id = ?", (send_time, art_id))

        def delete(art_id: int):
            """Удаление арта из БД

            Args:
                art_id (int): ID арта
            """
            DBWorker.execute("DELETE FROM arts WHERE id = ?", (art_id, ))
            DBWorker.PostFiles.delete(art_id)
    
        def get_all():
            """Получение всех артов

            Returns:
                data (list): Список артов
            """
            data = DBWorker.execute("SELECT * FROM arts", ())
            return data
        
        def get_with_timer():
            """Получение всех артов с установленным таймером

            Returns:
                art_list (list | None): Список артов
            """
            data = DBWorker.execute("SELECT * FROM arts WHERE state = 'accept'", ())
            return data
