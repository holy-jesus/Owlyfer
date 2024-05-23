import configparser


LOG_PATH = "logs/"
SETTINGS_PATH = "data/settings.ini"
DB_PATH = "data/database.db"

#Загрузка настроек
try:
    config = configparser.ConfigParser()
    config.read(SETTINGS_PATH)

    BOT_TOKEN = config.get("telegram", "bot_token")
    CHANNEL_ID = config.get("telegram", "channel_id")
except:
    print("Ошибка загрузки параметров, проверьте верность введенных данных")
    exit()