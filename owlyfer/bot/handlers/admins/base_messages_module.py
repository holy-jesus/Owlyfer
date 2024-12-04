from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards import (
    button_base_messages,
    keyboard_base_messages_menu,
    button_message_edit,
    keyboard_message_edit_select,
    button_stop,
    button_edit_message_ban,
    button_edit_message_help,
    button_edit_message_welcome,
    button_edit_message_post,
    keyboard_stop,
    button_message_show,
)
from bot.loader import dp, db
from .admin_filter import IsAdmin


class EditBaseMessageState(StatesGroup):
    get_message_type = State()
    get_message_text = State()


class ShowBaseMessageState(StatesGroup):
    get_message_type = State()


@dp.message(IsAdmin, F.text == button_base_messages.text)
async def base_message_menu(message: Message):
    await message.answer(
        "Меню редактирования базовых сообщений",
        reply_markup=keyboard_base_messages_menu,
    )


@dp.message(IsAdmin, F.text == button_message_edit.text)
async def edit_base_message_start(message: Message, state: FSMContext):
    await message.answer(
        "Выберите сообщение, которое хотите отредактировать",
        reply_markup=keyboard_message_edit_select,
    )
    await state.set_state(EditBaseMessageState.get_message_type)


@dp.message(IsAdmin, EditBaseMessageState.get_message_type, F.text == button_stop.text)
async def edit_base_message_stop(message: Message, state: FSMContext):
    await message.answer(
        "Отмена изменения базовых сообщений", reply_markup=keyboard_base_messages_menu
    )
    await state.clear()


@dp.message(IsAdmin, EditBaseMessageState.get_message_type)
async def edit_base_message_get_type(message: Message, state: FSMContext):
    message_type = message.text
    message_text = "Отправьте текст сообщения"
    if message_type in [
        button_edit_message_ban.text,
        button_edit_message_help.text,
        button_edit_message_welcome.text,
    ]:
        message_text += "\n\n<i>Для добавления ника пользователя в сообщение используйте $USERNAME$</i>"
    if message_type not in [
        button_edit_message_ban.text,
        button_edit_message_help.text,
        button_edit_message_welcome.text,
        button_edit_message_post.text,
    ]:
        await message.answer("Данный тип сообщения не найден, повторите выбор")
        return
    await state.update_data(message_type=message_type)
    await message.answer(message_text, reply_markup=keyboard_stop)
    await state.set_state(EditBaseMessageState.get_message_text)


@dp.message(IsAdmin, EditBaseMessageState.get_message_text)
async def edit_base_message_get_text(message: Message, state: FSMContext):
    message_types = {
        button_edit_message_welcome.text: "welcome",
        button_edit_message_help.text: "help",
        button_edit_message_post.text: "post",
        button_edit_message_ban.text: "ban",
    }
    data = await state.get_data()
    message_type = message_types[data["message_type"]]
    db.MsgTemplates.edit(message_type, message.html_text)
    await message.answer(
        "Базовое сообщение изменено", reply_markup=keyboard_base_messages_menu
    )
    await state.clear()


@dp.message(IsAdmin, F.text == button_message_show.text)
async def show_base_message_start(message: Message, state: FSMContext):
    await message.answer(
        "Выберите базовое сообщение для отображения",
        reply_markup=keyboard_message_edit_select,
    )
    await state.set_state(ShowBaseMessageState.get_message_type)


@dp.message(IsAdmin, ShowBaseMessageState.get_message_type, F.text == button_stop.text)
async def show_base_message_stop(message: Message, state: FSMContext):
    await message.answer(
        "Отмена показа сообщения", reply_markup=keyboard_base_messages_menu
    )
    await state.clear()


@dp.message(IsAdmin, ShowBaseMessageState.get_message_type)
async def show_base_message_get_type(message: Message, state: FSMContext):
    message_type = message.text
    if message_type == button_edit_message_ban.text:
        base_message_type = "ban"
    elif message_type == button_edit_message_help.text:
        base_message_type = "help"
    elif message_type == button_edit_message_welcome.text:
        base_message_type = "welcome"
    elif message_type == button_edit_message_post.text:
        base_message_type = "post"
    else:
        await message.answer("Данный тип сообщения не найдет, повторите выбор")
        return
    message_text = db.MsgTemplates.get(base_message_type)
    message_text = message_text.replace("$USERNAME$", message.from_user.first_name)
    await message.answer(message_text)
    await message.answer("Возврат в меню", reply_markup=keyboard_base_messages_menu)
    await state.clear()
