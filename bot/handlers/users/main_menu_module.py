from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from bot.keyboards import keyboard_main, button_user_help, button_about_bot
from bot.loader import dp, db


@dp.message(CommandStart())
async def hello_message(message: Message):
    if db.Users.get_by_tg_id(message.from_user.id) == None:
        db.Users.add(message.from_user.id)
    msg_text = db.MsgTemplates.get("welcome")
    msg_text = msg_text.replace("$USERNAME$", message.from_user.first_name)
    await message.answer(msg_text, reply_markup=keyboard_main)


@dp.message(F.text == button_user_help.text)
@dp.message(Command("help"))
async def help_message(message: Message):
    msg_text = db.MsgTemplates.get("help")
    msg_text = msg_text.replace("$USERNAME$", message.from_user.first_name)
    await message.answer(msg_text)


@dp.message(F.text == button_about_bot.text)
@dp.message(Command("about"))
async def about_bot_message(message: Message):
    await message.answer("""<a href="https://github.com/holy-jesus/Owlyfer">Owlyfer</a>

Оригинальный создатель бота Knotoni.
Обновил и захостил @ho1y_jesus""", disable_web_page_preview=True)
