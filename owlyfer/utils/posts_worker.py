import asyncio
import datetime

from aiogram.enums import ParseMode
from aiogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    InputMediaDocument,
    InputMediaAudio,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.loader import bot, db
from utils.log_worker import Logger
from utils.settings_loader import CHANNEL_ID


class post_vote(CallbackData, prefix="pv"):
    post_id: int
    action: str
    disable_notification: bool = True


class post_select_time(CallbackData, prefix="pst"):
    post_id: int
    hour: int
    action: str
    disable_notification: bool = True


def create_post_buttons(post_id: int):
    button_accept_post = InlineKeyboardButton(
        text="Принять", callback_data=post_vote(post_id=post_id, action="accept").pack()
    )
    button_decline_post = InlineKeyboardButton(
        text="Отклонить",
        callback_data=post_vote(post_id=post_id, action="decline").pack(),
    )
    button_ban_user = InlineKeyboardButton(
        text="Забанить юзера",
        callback_data=post_vote(post_id=post_id, action="ban").pack(),
    )
    keyboard_post_vote = (
        InlineKeyboardBuilder()
        .add(button_accept_post, button_decline_post, button_ban_user)
        .as_markup()
    )
    return keyboard_post_vote


async def create_media_group_to_post(post_id: int, caption: str | None) -> list:
    """Создание медиа группы для отправки

    Args:
        post_id (int): ID поста
        caption (str | None): текст поста

    Returns:
        media_list (str | None): медиа группа (None при отсутствии файлов в посте)
    """
    post_files = db.PostFiles.get(post_id)
    if post_files == None:
        return None
    media_list = []
    file_classes = {
        "img": InputMediaPhoto,
        "vid": InputMediaVideo,
        "gif": InputMediaAnimation,
        "doc": InputMediaDocument,
        "mus": InputMediaAudio,
    }
    for i in post_files:
        file_class = file_classes.get(i[2])
        if not file_class:
            continue
        media_list.append(
            file_class(media=i[3], caption=caption, parse_mode=ParseMode.HTML)
        )
        caption = None
    return media_list


async def send_post_to_admins(post_id: int):
    """
    Рассылает предложенный пост всем админам

    Args:
        post_id (int): ID поста
    """
    post = db.Posts.get(post_id)
    user_tg_id = db.Users.get_by_db_id(post[1])
    user = await bot.get_chat(user_tg_id)
    admins = db.Admins.get_all()
    if post[2] != None:
        post_text = post[2] + f"\n<i>Предложил(а) - {user.first_name}</i>"
    else:
        post_text = f"<i>Предложил(а) - {user.first_name}</i>"
    media_list = await create_media_group_to_post(post_id, post_text)
    keyboard_post_vote = create_post_buttons(post_id)
    for i in admins:
        try:
            if media_list != None:
                message = await bot.send_media_group(i[1], media_list)

                reply = await message[0].reply(
                    "Что сделать с постом?", reply_markup=keyboard_post_vote
                )
            else:
                message = await bot.send_message(i[1], post_text)
                reply = await message.reply(
                    "Что сделать с постом?", reply_markup=keyboard_post_vote
                )

            db.AdminPostStates.add(post_id, i[0], reply.message_id)
        except Exception as ex:
            Logger.error(ex)
            continue


async def send_post_to_channel(post_id: int, disable_notification: bool = True):
    """
    Отправляет одобренный пост в канал

    Args:
        post_id (int): ID поста
        disable_notification (bool): Отключает уведомление
    """
    post = db.Posts.get(post_id)
    user_tg_id = db.Users.get_by_db_id(post[1])
    user = await bot.get_chat(user_tg_id)
    post_template = db.MsgTemplates.get("post")
    if post[2] == None:
        post_text = f"<i>Предложил(а) - {user.first_name}</i>\n" + post_template
    else:
        post_text = (
            post[2] + f"\n\n<i>Предложил(а) - {user.first_name}</i>\n" + post_template
        )
    media_group = await create_media_group_to_post(post_id, post_text)
    if media_group == None:
        await bot.send_message(CHANNEL_ID, post_text, disable_notification=disable_notification)
    else:
        await bot.send_media_group(CHANNEL_ID, media_group, disable_notification=disable_notification)
    db.Posts.delete(post_id)


async def set_delayed_post_send(post_id: int, hour: int, disable_notification: bool):
    send_date = datetime.datetime.now() + datetime.timedelta(hours=hour)
    db.Posts.accept(post_id, send_date, disable_notification)


async def send_delayed_posts():
    while True:
        delayed_posts = db.Posts.get_with_timer()
        if delayed_posts != None:
            for post in delayed_posts:
                if post[3] == "accept":
                    send_date = datetime.datetime.strptime(post[4], "%d-%m-%Y %H:%M")
                    if send_date <= datetime.datetime.now():
                        await send_post_to_channel(post[0], post[5])
                        db.Posts.delete(post[0])
        await asyncio.sleep(300)
