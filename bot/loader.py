from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils.log_worker import Logger
from utils.db_worker import DBWorker
from utils.settings_loader import BOT_TOKEN


try:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    db = DBWorker()
except Exception as ex:
    Logger.error(ex)
    exit()
