import telebot
from telebot.types import InlineKeyboardMarkup
from keyboards.keyboards import get_start_menu_buttons, get_under_menu_buttons
from processors.bot_talks import BotTalks
from database.cache import DatabaseCache
from comon_functions.lprint import lprint


def send_welcome(message: telebot.types.Message, bot: telebot.TeleBot):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*get_start_menu_buttons())
    try:
        res = DatabaseCache.add_user(message.from_user.id, message.from_user.username,
                                     message.from_user.first_name, message.from_user.last_name,
                                     message.from_user.is_premium)
        keyb = get_under_menu_buttons() # Почему полностью не написали?
        if res is True:
            BotTalks.dialogues_new_message(
                F"Новый пользователь ({message.from_user.first_name} {message.from_user.last_name})\nID: {message.from_user.id}\nUN: @{message.from_user.username}"
            )
        bot.send_message(
            message.chat.id,
            DatabaseCache.get_special_project_parameters(
                jinja=True).get('BOT_WELCOME_MESSAGE_description'), reply_markup=keyb)
        secnd_msg = DatabaseCache.get_special_project_parameters( # Тоже сократили? Или опечатка?
            jinja=True).get('BOT_WELCOME_MESSAGE_extra_field_1')
        if len(secnd_msg) > 1:
            bot.send_message(message.chat.id, secnd_msg, reply_markup=markup)
    except Exception as e:
        lprint.p("Error on send_welcome", e)
