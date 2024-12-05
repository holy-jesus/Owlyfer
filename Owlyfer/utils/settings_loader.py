import configparser
import traceback


LOG_PATH = "logs/"
SETTINGS_PATH = "settings.ini"
DB_PATH = "database.db"

# Загрузка настроек
try:
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(SETTINGS_PATH)

    BOT_TOKEN = config.get("telegram", "bot_token")
    CHANNEL_ID = config.get("telegram", "channel_id")
    MONGODB_HOST = config.get("mongodb", "host", fallback="127.0.0.1")
    MONGODB_PORT = int(config.get("mongodb", "port", fallback="27017"))
    MONGODB_USERNAME = config.get("mongodb", "username") or None
    MONGODB_PASSWORD = config.get("mongodb", "password") or None
except Exception as e:
    print(traceback.format_exc())
    print("Ошибка загрузки параметров, проверьте верность введенных данных")
    exit()
