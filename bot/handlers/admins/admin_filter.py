from aiogram.types import Message, CallbackQuery

from bot.loader import db


def IsAdmin(data: Message | CallbackQuery):
    return db.Admins.get_by_tg_id(data.from_user.id) != None
