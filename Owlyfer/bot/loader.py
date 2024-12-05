from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.mongo import MongoStorage
from motor.motor_asyncio import AsyncIOMotorClient

from utils.log_worker import Logger
from utils.db_worker import DBWorker
from utils.settings_loader import (
    BOT_TOKEN,
    MONGODB_HOST,
    MONGODB_PORT,
    MONGODB_USERNAME,
    MONGODB_PASSWORD,
)
from db import DBSessionMiddleware, async_session_factory


try:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    client = AsyncIOMotorClient(
        host=MONGODB_HOST,
        port=MONGODB_PORT,
        username=MONGODB_USERNAME,
        password=MONGODB_PASSWORD,
        connect=True,
    )
    dp = Dispatcher(storage=MongoStorage(client=client, db_name="owlyfer"))
    dp.message.middleware(DBSessionMiddleware(async_session_factory))
    db = DBWorker()
except Exception as ex:
    Logger.error(ex)
    exit()
