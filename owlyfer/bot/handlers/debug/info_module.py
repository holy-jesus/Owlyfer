from aiogram.types import Message
from aiogram.filters import Command

from bot.loader import dp


@dp.message(Command("debug"))
async def debug_info(message: Message):
    await message.answer(
        "<b>Техническая информация</b>\n\n"
        + f"Telegram ID - <code>{message.from_user.id}</code>\n"
        + f"Username - <code>{message.from_user.username}</code>"
    )
