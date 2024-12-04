from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards import keyboard_admin, button_a_main_menu, button_admin_help
from bot.loader import dp
from .admin_filter import IsAdmin


@dp.message(IsAdmin, Command("admin"))
async def admin_menu(message: Message):
    await message.answer(
        f"Добро пожаловать в меню админа, {message.from_user.first_name}",
        reply_markup=keyboard_admin,
    )


@dp.message(IsAdmin, F.text == button_a_main_menu.text)
async def return_to_admin_menu(message: Message):
    await message.answer("Возврат в главное меню", reply_markup=keyboard_admin)


@dp.message(IsAdmin, F.text == button_admin_help.text)
async def admin_help(message: Message):
    message_text = "text"
    await message.answer(message_text)
