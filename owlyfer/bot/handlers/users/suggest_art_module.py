from aiogram import F
from aiogram.types import Message, ContentType
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards import (
    keyboard_next_stop,
    keyboard_main,
    button_create_post,
    button_stop,
    button_next,
)
from bot.loader import dp, db
from utils.posts_worker import send_post_to_admins


class SuggestPostState(StatesGroup):
    get_post = State()


@dp.message(F.text == button_create_post.text)
async def suggest_post_start(message: Message, state: FSMContext):
    ban_state = db.Users.get_ban_state(message.from_user.id)
    if ban_state == True:
        message_text = db.MsgTemplates.get("ban").replace(
            "$USERNAME$", message.from_user.first_name
        )
        await message.answer(message_text)
        return
    await message.answer(
        "Отправьте сформированный пост, после чего нажмите 'Далее'",
        reply_markup=keyboard_next_stop,
    )
    await state.set_state(SuggestPostState.get_post)


@dp.message(SuggestPostState.get_post, F.text == button_stop.text)
async def suggest_post_break(message: Message, state: FSMContext):
    data = await state.get_data()
    if "post_id" in data:
        db.Posts.delete(data["post_id"])
    await message.answer("Отмена отправки поста", reply_markup=keyboard_main)
    await state.clear()


@dp.message(
    SuggestPostState.get_post,
    or_f(F.photo, F.document, F.video, F.audio, F.text),
    F.text != button_next.text,
)
async def suggest_post_process(message: Message, state: FSMContext):
    data = await state.get_data()
    if "post_id" not in data:
        post_id = db.Posts.add(message.from_user.id, message.html_text or None)
    else:
        post_id = data["post_id"]
    
    media_group_id = data.get("media_group_id", message.media_group_id)
    if message.html_text:
        db.Posts.update(post_id, message.html_text)
    if message.media_group_id is None or message.media_group_id != media_group_id:
        db.PostFiles.delete(post_id)

    await state.update_data(media_group_id=message.media_group_id, post_id=post_id)
    match message.content_type:
        case ContentType.PHOTO:
            db.PostFiles.add(post_id, message.photo[-1].file_id, "img")
        case ContentType.DOCUMENT:
            db.PostFiles.add(post_id, message.document.file_id, "doc")
        case ContentType.VIDEO:
            db.PostFiles.add(post_id, message.video.file_id, "vid")


@dp.message(SuggestPostState.get_post, F.text == button_next.text)
async def suggest_post_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    if "post_id" not in data:
        return await message.answer("Вы не отправили пост")
    post_id = data["post_id"]
    db.Posts.suggest(post_id)
    await message.answer(
        f"Пост принят\nID вашего поста - {post_id}", reply_markup=keyboard_main
    )
    await send_post_to_admins(post_id)
    await state.clear()

