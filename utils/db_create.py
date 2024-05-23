import sqlite3
from utils.settings_loader import DB_PATH
from utils.log_worker import Logger


def create_database():
    try:
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            telegram_id INTEGER UNIQUE NOT NULL,
                            ban_state INTEGER NOT NULL
                        )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS admins (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            telegram_id INTEGER UNIQUE NOT NULL,
                            nickname TEXT NOT NULL
                        )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS msg_templates (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            msg_type TEXT UNIQUE NOT NULL,
                            msg_text TEXT NOT NULL
                        )"""
        )

        cursor.execute(
            """INSERT INTO msg_templates (msg_type, msg_text) VALUES (?, ?)""",
            ("welcome", 'Добро пожаловать'),
        )
        cursor.execute(
            """INSERT INTO msg_templates (msg_type, msg_text) VALUES (?, ?)""",
            (
                "help",
                """Правила""",
            ),
        )
        cursor.execute(
            """INSERT INTO msg_templates (msg_type, msg_text) VALUES (?, ?)""",
            ("post", "Предложить пост"),
        )
        cursor.execute(
            """INSERT INTO msg_templates (msg_type, msg_text) VALUES (?, ?)""",
            ("ban", "Вы забанены"),
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS posts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            post_text TEXT,
                            state TEXT NOT NULL,
                            send_date TEXT,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS post_files (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            post_id INTEGER NOT NULL,
                            file_type TEXT NOT NULL,
                            file_id TEXT NOT NULL,
                            FOREIGN KEY (post_id) REFERENCES posts (id)
                        )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS admin_post_states (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            admin_id INTEGER NOT NULL,
                            post_id INTEGER NOT NULL,
                            msg_id INTEGER NOT NULL,
                            FOREIGN KEY (admin_id) REFERENCES admins (id),
                            FOREIGN KEY (post_id) REFERENCES posts (id)
                        )"""
        )

        con.commit()
        con.close()
        Logger.info("Database and tables created successfully.")
    except Exception as ex:
        Logger.error(f"Error creating database: {ex}")
        raise ex


if __name__ == "__main__":
    create_database()
