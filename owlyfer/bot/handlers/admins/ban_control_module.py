from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards import (
    button_bans,
    keyboard_ban_menu,
    button_ban_user,
    keyboard_stop,
    button_stop,
    button_unban_user,
)
from bot.loader import dp, db
from .admin_filter import IsAdmin


class BanUserState(StatesGroup):
    get_tg_id = State()


class UnbanUserState(StatesGroup):
    get_tg_id = State()


@dp.message(IsAdmin, F.text == button_bans.text)
async def ban_control_menu(message: Message):
    await message.answer("Меню банов и блокировок", reply_markup=keyboard_ban_menu)


@dp.message(IsAdmin, F.text == button_ban_user.text)
async def ban_user_start(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте Telegram ID юзера, которого нужно забанить",
        reply_markup=keyboard_stop,
    )
    await state.set_state(BanUserState.get_tg_id)


@dp.message(IsAdmin, BanUserState.get_tg_id, F.text == button_stop.text)
async def ban_user_stop(message: Message, state: FSMContext):
    await message.answer("Отмена бана юзера", reply_markup=keyboard_ban_menu)
    await state.clear()


@dp.message(IsAdmin, BanUserState.get_tg_id)
async def ban_user_get_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Неверный ID, попробуйте снова")
        return
    tg_id = int(message.text)
    user = db.Users.get_by_tg_id(tg_id)
    if user == None:
        await message.answer("Пользователь не найден, попробуйте снова")
        return
    db.Users.edit_ban_state(tg_id, True)
    await message.answer(f"Юзер забанен", reply_markup=keyboard_ban_menu)
    await state.clear()


@dp.message(F.text == button_unban_user.text)
async def unban_user_start(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте Telegram ID юзера, которого требуется разбанить",
        reply_markup=keyboard_stop,
    )
    await state.set_state(UnbanUserState.get_tg_id)


@dp.message(IsAdmin, UnbanUserState.get_tg_id, F.text == button_stop.text)
async def unban_user_stop(message: Message, state: FSMContext):
    await message.answer("Отмена разбана юзера", reply_markup=keyboard_ban_menu)
    await state.clear()


@dp.message(IsAdmin, UnbanUserState.get_tg_id)
async def unban_user_get_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Неверный ID, попробуйте снова")
        return
    tg_id = int(message.text)
    user = db.Users.get_by_tg_id(tg_id)
    if user == None:
        await message.answer("Пользователь не найден, попробуйте снова")
        return
    db.Users.edit_ban_state(tg_id, False)
    await message.answer(f"Юзер разбанен", reply_markup=keyboard_ban_menu)
    await state.clear()
