from aiogram import F
from emoji import emojize
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.exceptions import AiogramError
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.posts_worker import (
    send_post_to_channel,
    set_delayed_post_send,
    create_post_buttons,
    post_vote,
    post_select_time,
)
from bot.loader import dp, db, bot
from utils.log_worker import Logger
from .admin_filter import IsAdmin


def create_hour_selection(post_id: int):
    keyboard_select_time = InlineKeyboardBuilder()
    for i in range(1, 13):
        keyboard_select_time.button(
            text=emojize(f":timer_clock: {i}"),
            callback_data=post_select_time(
                post_id=post_id, action="send", hour=i
            ).pack(),
        )
    keyboard_select_time.button(
        text="Отмена",
        callback_data=post_vote(action="break", post_id=post_id).pack(),
    )
    return keyboard_select_time.adjust(6, 6, 1).as_markup()


def create_time_selection(post_id: int):
    button_send_now = InlineKeyboardButton(
        text="Сейчас",
        callback_data=post_vote(action="send_now", post_id=post_id).pack(),
    )
    button_send_later = InlineKeyboardButton(
        text="Позже",
        callback_data=post_vote(action="send_later", post_id=post_id).pack(),
    )
    button_cancel = InlineKeyboardButton(
        text="Отмена", callback_data=post_vote(action="break", post_id=post_id).pack()
    )
    return (
        InlineKeyboardBuilder()
        .add(button_send_now, button_send_later, button_cancel)
        .as_markup()
    )


@dp.callback_query(IsAdmin, post_vote.filter(F.action == "decline"))
async def decline_post(query: CallbackQuery, callback_data: post_vote):
    post_id = callback_data.post_id
    admin_list = db.Admins.get_all()
    admin_nick = db.Admins.get_nick(query.from_user.id)
    for i in admin_list:
        try:
            msg_id = db.AdminPostStates.get_msg_id(post_id, i[0])
            await bot.edit_message_text(
                f"{admin_nick} отклонил(а) пост", i[1], msg_id, reply_markup=None
            )
        except AiogramError as ex:
            Logger.error(ex)
            continue
    db.AdminPostStates.delete(post_id)
    post = db.Posts.get(post_id)
    user_tg_id = db.Users.get_by_db_id(post[1])
    await bot.send_message(
        user_tg_id, f"Ваш пост отклонили\nID поста - <b>{post_id}</b>"
    )
    db.Posts.delete(post_id)


@dp.callback_query(IsAdmin, post_vote.filter(F.action == "ban"))
async def ban_user_and_decline_post(query: CallbackQuery, callback_data: post_vote):
    post_id = callback_data.post_id
    post = db.Posts.get(post_id)
    user_tg_id = db.Users.get_by_db_id(post[1])
    user = await bot.get_chat(user_tg_id)
    admin_list = db.Admins.get_all()
    admin_nick = db.Admins.get_nick(query.from_user.id)
    for i in admin_list:
        try:
            msg_id = db.AdminPostStates.get_msg_id(post_id, i[0])
            await bot.edit_message_text(
                f"{admin_nick} отклонил(а) пост и забанил(а) {user.first_name}",
                i[1],
                msg_id,
                reply_markup=None,
            )
        except AiogramError as ex:
            Logger.error(ex)
            continue
    db.AdminPostStates.delete(post_id)
    db.Users.edit_ban_state(user_tg_id, True)
    await bot.send_message(
        user_tg_id, f"Вы были забанены за пост\nID поста - <b>{post_id}</b>"
    )
    db.Posts.delete(post_id)


@dp.callback_query(IsAdmin, post_vote.filter(F.action == "accept"))
async def accept_post(query: CallbackQuery, callback_data: post_vote):
    post_id = callback_data.post_id
    keyboard_send_time = create_time_selection(post_id)
    admin_id = db.Admins.get_by_tg_id(query.from_user.id)
    msg_id = db.AdminPostStates.get_msg_id(post_id, admin_id)
    await bot.edit_message_text(
        "Когда отправить пост?",
        query.from_user.id,
        msg_id,
        reply_markup=keyboard_send_time,
    )


@dp.callback_query(IsAdmin, post_vote.filter(F.action == "break"))
async def back_to_select_post_action(query: CallbackQuery, callback_data: post_vote):
    post_id = callback_data.post_id
    keyboard_post_vote = create_post_buttons(post_id)
    admin_id = db.Admins.get_by_tg_id(query.from_user.id)
    msg_id = db.AdminPostStates.get_msg_id(post_id, admin_id)
    await bot.edit_message_text(
        "Что сделать с постом?",
        query.from_user.id,
        msg_id,
        reply_markup=keyboard_post_vote,
    )


@dp.callback_query(IsAdmin, post_vote.filter(F.action == "send_now"))
async def accept_post_send_now(query: CallbackQuery, callback_data: post_vote):
    post_id = callback_data.post_id
    post = db.Posts.get(post_id)
    user_tg_id = db.Users.get_by_db_id(post[1])
    await send_post_to_channel(post_id)
    admin_list = db.Admins.get_all()
    admin_nick = db.Admins.get_nick(query.from_user.id)
    await bot.send_message(
        user_tg_id, f"Ваш пост приняли!\nID поста - <b>{post_id}</b>"
    )
    for i in admin_list:
        try:
            msg_id = db.AdminPostStates.get_msg_id(post_id, i[0])
            await bot.edit_message_text(
                f"{admin_nick} принял(а) пост", i[1], msg_id, reply_markup=None
            )
        except AiogramError as ex:
            Logger.error(ex)
            continue
    db.Posts.delete(post_id)
    db.AdminPostStates.delete(post_id)


@dp.callback_query(IsAdmin, post_vote.filter(F.action == "send_later"))
async def accept_post_select_time(query: CallbackQuery, callback_data: post_vote):
    post_id = callback_data.post_id
    keyboard_select_time = create_hour_selection(post_id)
    admin_tg_id = db.Admins.get_by_tg_id(query.from_user.id)
    msg_id = db.AdminPostStates.get_msg_id(post_id, admin_tg_id)
    await bot.edit_message_text(
        "Через сколько часов отправить пост?",
        query.from_user.id,
        msg_id,
        reply_markup=keyboard_select_time,
    )


@dp.callback_query(IsAdmin, post_select_time.filter(F.action == "send"))
async def accept_post_send_later(query: CallbackQuery, callback_data: post_select_time):
    post_id = callback_data.post_id
    hour = callback_data.hour
    await set_delayed_post_send(post_id, hour)
    admin_list = db.Admins.get_all()
    admin_nick = db.Admins.get_nick(query.from_user.id)
    post = db.Posts.get(post_id)
    user_tg_id = db.Users.get_by_db_id(post[1])
    await bot.send_message(user_tg_id, f"Ваш пост приняли! ID поста - <b>{post_id}</b>")
    for i in admin_list:
        try:
            msg_id = db.AdminPostStates.get_msg_id(post_id, i[0])
            await bot.edit_message_text(
                f"{admin_nick} запланировал(а) отправку поста через {hour} час(ов)",
                i[1],
                msg_id,
                reply_markup=None,
            )
        except AiogramError as ex:
            Logger.error(ex)
            continue
    db.AdminPostStates.delete(post_id)
