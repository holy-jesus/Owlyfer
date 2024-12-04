from aiogram import F
from aiogram.types import Message
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards import button_mass_send, keyboard_stop, button_stop, keyboard_admin
from bot.loader import dp, db
from .admin_filter import IsAdmin


class MassSendState(StatesGroup):
    get_message = State()


@dp.message(IsAdmin, F.text == button_mass_send.text)
async def mass_send_start(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте сообщение для массовой рассылки", reply_markup=keyboard_stop
    )
    await state.set_state(MassSendState.get_message)


@dp.message(IsAdmin, MassSendState.get_message, F.text == button_stop.text)
async def mass_send_stop(message: Message, state: FSMContext):
    await message.answer("Отмена массовой рассылки", reply_markup=keyboard_admin)
    await state.clear()


@dp.message(IsAdmin, MassSendState.get_message)
async def mass_send_final(message: Message, state: FSMContext):
    user_list = db.Users.get_all()
    for i in user_list:
        if i[1] != message.from_user.id:
            try:
                await message.send_copy(i[1])
            except AiogramError:
                continue
    await message.answer("Сообщение разослано", reply_markup=keyboard_admin)
    await state.clear()
