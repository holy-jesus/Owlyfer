from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards import (
    button_admins,
    keyboard_admin_menu,
    button_show_admins,
    button_add_admin,
    keyboard_stop,
    button_stop,
    button_delete_admin,
)
from bot.loader import dp, db, bot
from .admin_filter import IsAdmin


class AddAdminState(StatesGroup):
    get_tg_id = State()
    get_nickname = State()


class DelAdminState(StatesGroup):
    get_tg_id = State()


@dp.message(IsAdmin, F.text == button_admins.text)
async def admin_control_menu(message: Message):
    await message.answer(
        "Меню управление администраторами", reply_markup=keyboard_admin_menu
    )


@dp.message(IsAdmin, F.text == button_show_admins.text)
async def admin_show_list(message: Message):
    admin_list = db.Admins.get_all()
    text = "<b>Список администраторов</b>\n\n"
    for i in admin_list:
        text += f"{i[2]} [<code>{i[1]}</code>]\n"
    await message.answer(text)


@dp.message(IsAdmin, F.text == button_add_admin.text)
async def add_admin_start(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте Telegram ID юзера, "
        + "которого хотите добавить в список администраторов\n"
        + "<i>Получить Telegram ID можно командой /debug</i>",
        reply_markup=keyboard_stop,
    )
    await state.set_state(AddAdminState.get_tg_id)


@dp.message(IsAdmin, AddAdminState.get_nickname, F.text == button_stop.text)
async def add_admin_stop(message: Message, state: FSMContext):
    await message.answer("Отмена добавления админа", reply_markup=keyboard_admin_menu)
    await state.clear()


@dp.message(AddAdminState.get_tg_id)
async def add_admin_get_tg_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Неверный ID, попробуйте снова")
        return
    tg_id = int(message.text)
    user = await bot.get_chat(tg_id)
    await message.answer(
        f"Пользователь - {user.first_name}\n"
        + "Отправьте ник, под которым его требуется добавить в админы"
    )
    await state.update_data(tg_id=tg_id)
    await state.set_state(AddAdminState.get_nickname)


@dp.message(IsAdmin, AddAdminState.get_nickname)
async def add_admin_get_nick(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = int(data["tg_id"])
    db.Admins.add(tg_id, message.text)
    await message.answer(
        f"Админ {message.text} добавлен", reply_markup=keyboard_admin_menu
    )
    await state.clear()


@dp.message(IsAdmin, F.text == button_delete_admin.text)
async def delete_admin_start(message: Message, state: FSMContext):
    await message.answer(
        "Введите Telegram ID админа, которого хотите удалить\n"
        + "<i>Получить его можно в списке администраторов</i>"
    )
    await state.set_state(DelAdminState.get_tg_id)


@dp.message(IsAdmin, DelAdminState.get_tg_id, F.text == button_stop.text)
async def delete_admin_stop(message: Message, state: FSMContext):
    await message.answer("Отмена удаления админа", reply_markup=keyboard_admin_menu)
    await state.clear()


@dp.message(IsAdmin, DelAdminState.get_tg_id)
async def delete_admin_get_tg_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Неверный ID, попробуйте снова")
        return
    tg_id = int(message.text)
    admin = db.Admins.get_by_tg_id(tg_id)
    if admin == None:
        await message.answer("Админ не найден, повторите ввод")
        return
    nick = db.Admins.get_nick(tg_id)
    db.Admins.delete(tg_id)
    await message.answer(f"Админ {nick} удален", reply_markup=keyboard_admin_menu)
    await state.finish()
