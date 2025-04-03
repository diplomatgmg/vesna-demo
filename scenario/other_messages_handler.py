import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from processors.bot_talks import BotTalks
from comon_functions.lprint import lprint
from database.cache import DatabaseCache
from keyboards.keyboards import get_under_menu_buttons_text


moderators_user = {}


def moderator_exit_handler(message: telebot.types.Message, bot: telebot.TeleBot):
    try:
        if message.from_user.id in moderators_user:
            user_chat_id = moderators_user[message.from_user.id]
            del moderators_user[message.from_user.id]
            bot.send_message(user_chat_id, "Модератор отключился.")
            bot.send_message(message.from_user.id, "Вы вышли из чата.")
    except Exception as e:
        lprint.p("moderator_exit_handler error", e)


def hadle_user_moderator_chat(message: telebot.types.Message, bot: telebot.TeleBot):
    try:
        if message.from_user.id in moderators_user.values():
            moderator_id = [k for k, v in moderators_user.items() if v == message.from_user.id][0]
            bot.forward_message(moderator_id, message.chat.id, message.message_id)
            return True
        if message.from_user.id in moderators_user:
            user_chat_id = moderators_user[message.from_user.id]
            bot.forward_message(user_chat_id, message.chat.id, message.message_id)
            return True
    except Exception as e:
        lprint.p("hadle_user_moderator_chat error", e)
    return False


def moderator_join_chat_hadler(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    try:
        if call.data.startswith("support_message_"):
            spp = DatabaseCache.get_special_project_parameters(jinja=True)
            admin_s = spp.get('MODERATOR_Telegram_IDs_value')
            if str(call.from_user.id) in admin_s:
                _, call_for_user = call.data.split(":")
                call_for_user = int(call_for_user)
                if call_for_user not in moderators_user.values():
                    moderators_user[call.from_user.id] = call_for_user
                    bot.send_message(call.from_user.id, F"Вы присоеденились к чату: {call_for_user}")
                    bot.send_message(call_for_user, F"Модератор {call.from_user.first_name} {call.from_user.last_name} присоеденился к чату.")
                else:
                    moderator_id = [k for k, v in moderators_user.items() if v == call_for_user][0]
                    bot.send_message(call.from_user.id, F"Пользователь {call_for_user} уже подключен к другому модератору {moderator_id}.")
    except Exception as e:
        lprint("moderator_join_chat_hadler error", e)


def create_response_support_message(message: telebot.types.Message):
    return F"""
Пользователь
User: {message.from_user.first_name} {message.from_user.last_name}
UserName: {F'@{message.from_user.username}' if message.from_user.username else 'НЕ УКАЗАН'}
ID: {message.from_user.id}
<strong>Запрашивает чат поддержки.</strong>
""".strip()


def handle_menu_buttons(message: telebot.types.Message, bot: telebot.TeleBot) -> bool:
    try:
        buttons_text: list = get_under_menu_buttons_text()
        for button in buttons_text:
            btn_cmd, btn_text = button.split("#") if len(button.split("#")) == 2 else [None, None]
            if message.text and message.text == btn_text:
                bot.delete_message(message.chat.id, message.message_id)
                spp = DatabaseCache.get_special_project_parameters(jinja=True)
                if btn_cmd == "sup":
                    button_textz = spp.get('under_menu_buttons_extra_field_1').split('\n')
                    message_text = [t for t in button_textz if t.startswith("sup#")]
                    if len(message_text) > 0:
                        BotTalks.send_message(message.chat.id, message_text[0].split("#")[1])
                        try:
                            admin_s = spp.get('MODERATOR_Telegram_IDs_value')
                            admin_s = admin_s.split(",") if "," in admin_s else [admin_s]
                            support_message = create_response_support_message(message)
                            for admin in admin_s:
                                if admin and int(admin) > 0:
                                    keyb = InlineKeyboardMarkup(row_width=1)
                                    keyb.add(InlineKeyboardButton(text='Присоедениться к чату', callback_data=F'support_message_:{message.from_user.id}'))
                                    bot.send_message(int(admin), support_message, reply_markup=keyb)
                        except Exception as e:
                            lprint.p("handle_menu_buttons error", e)
                return True
    except Exception as e:
        lprint.p("Error on handle_menu_buttons", e)
    return False


def handle_other_text(message: telebot.types.Message, bot: telebot.TeleBot):
    # process for user vs moderator chat
    if hadle_user_moderator_chat(message, bot):
        return
    # process for menu buttons
    if handle_menu_buttons(message, bot):
        return
    if message.text and message.from_user.id:
        BotTalks.add_message(bot, message.from_user.id, message.text)
        BotTalks.dialogues_new_message(
            F"ID: {message.from_user.id} @{message.from_user.username}\nTM: {message.text}")
    if message.voice and message.voice.file_id:
        try:
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_size_kb = len(downloaded_file) / 1024
            if file_size_kb < 21000:
                voice_file = ("voice.ogg", downloaded_file, "audio/ogg")
                lprint.p("Start converting voice to text", file_size_kb)
                res = BotTalks.voice_to_text(message.from_user.id, voice_file)
                if res:
                    lprint.p("Succesfully converted voice to text, sending to GPT", len(res))
                    BotTalks.add_message(bot, message.from_user.id, res)
                    BotTalks.dialogues_new_message(
                        F"ID: {message.from_user.id} @{message.from_user.username}\nVM: {res}")
            else:
                bot.send_message(message.chat.id,
                                 "Вы отправили слишком длинное голосовое сообщение")
        except Exception as e:
            lprint.p("Error receiving voice", e)
