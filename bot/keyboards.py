from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from emoji import emojize


# Базовые кнопки и клавиатуры

button_stop = KeyboardButton(text=emojize(":stop_sign: Отмена"))
button_main_menu = KeyboardButton(text=emojize(":compass: Главное меню"))
button_next = KeyboardButton(text=emojize(":large_orange_diamond: Далее"))
button_a_main_menu = KeyboardButton(text=emojize(":gear: В главное меню"))

keyboard_stop = (
    ReplyKeyboardBuilder().add(button_stop).adjust(1).as_markup(resize_keyboard=True)
)

keyboard_next_stop = (
    ReplyKeyboardBuilder()
    .add(button_stop, button_next)
    .adjust(2)
    .as_markup(resize_keyboard=True)
)

# Главное меню юзера

button_create_post = KeyboardButton(text=emojize(":incoming_envelope: Предложить пост"))
button_create_art = KeyboardButton(
    text=emojize(":artist_palette: Предложить арт на донат")
)
button_user_help = KeyboardButton(text=emojize(":thinking_face: Справка"))
button_about_bot = KeyboardButton(text=emojize(":owl: О боте"))

keyboard_main = (
    ReplyKeyboardBuilder()
    .add(button_create_post, button_create_art, button_user_help, button_about_bot)
    .adjust(1, repeat=True)
    .as_markup(resize_keyboard=True)
)

# Главное меню админа

button_base_messages = KeyboardButton(text=emojize(":envelope: Базовые сообщения"))
button_admins = KeyboardButton(text=emojize(":locked_with_key: Администраторы"))
button_bans = KeyboardButton(text=emojize(":hammer: Баны и блокировки"))
button_mass_send = KeyboardButton(text=emojize(":loudspeaker: Массовая рассылка"))
button_admin_help = KeyboardButton(text=emojize(":open_book: Справка"))

keyboard_admin = (
    ReplyKeyboardBuilder()
    .add(
        button_mass_send,
        button_admins,
        button_bans,
        button_base_messages,
        button_admin_help,
    )
    .adjust(1, repeat=True)
    .as_markup(resize_keyboard=True)
)

# Изменение базовых сообщений

button_message_edit = KeyboardButton(text=emojize(":pencil: Изменить сообщения"))
button_message_show = KeyboardButton(text=emojize(":memo: Показать сообщения"))

keyboard_base_messages_menu = (
    ReplyKeyboardBuilder()
    .add(button_message_edit, button_message_show, button_a_main_menu)
    .adjust(1, repeat=True)
    .as_markup(resize_keyboard=True)
)

button_edit_message_welcome = KeyboardButton(text="Приветственное сообщение")
button_edit_message_help = KeyboardButton(text="Помощь")
button_edit_message_post = KeyboardButton(text="Подпись к посту")
button_edit_message_ban = KeyboardButton(text="Сообщение забаненному")


keyboard_message_edit_select = (
    ReplyKeyboardBuilder()
    .add(
        button_edit_message_welcome,
        button_edit_message_help,
        button_edit_message_post,
        button_edit_message_ban,
        button_stop,
    )
    .adjust(1, repeat=True)
    .as_markup(resize_keyboard=True)
)

button_show_admins = KeyboardButton(text=emojize(":scroll: Список администраторов"))
button_add_admin = KeyboardButton(text=emojize(":key: Добавить администратора"))
button_delete_admin = KeyboardButton(text=emojize(":locked: Удалить администратора"))

keyboard_admin_menu = (
    ReplyKeyboardBuilder()
    .add(button_show_admins, button_add_admin, button_delete_admin, button_a_main_menu)
    .adjust(1, repeat=1)
    .as_markup(resize_keyboard=True)
)


button_ban_user = KeyboardButton(text=emojize(":kitchen_knife: Забанить юзера"))
button_unban_user = KeyboardButton(text=emojize(":recycling_symbol: Разбанить юзера"))

keyboard_ban_menu = (
    ReplyKeyboardBuilder()
    .add(button_ban_user, button_unban_user, button_a_main_menu)
    .adjust(1, repeat=1)
    .as_markup(resize_keyboard=True)
)
