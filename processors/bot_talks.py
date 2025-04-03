import telebot
from chatgpt_md_converter import telegram_format
from database.cache import DatabaseCache
from comon_functions.gigachat import GigaChat
from comon_functions.chatgpt import ChatGpt # Ошибка импорта
from comon_functions.lprint import lprint
from keyboards.keyboards import get_under_menu_buttons


class BotTalks:
    _bot = None

    @classmethod
    def init(cls, bot: telebot.TeleBot):
        cls._bot = bot

    @classmethod
    def send_action(cls, chat_id):
        try:
            cls._bot.send_chat_action(chat_id, action='typing', timeout=10)
        except Exception as e:
            lprint.p("Error on send chat action", e)

    @classmethod
    def add_message(cls, bot: telebot.TeleBot, user_id, message):
        spp = DatabaseCache.get_special_project_parameters(jinja=True)
        ai_system = spp.get('ai_system_value')
        ai_prompt = spp.get('ai_system_extra_field_1')

        if ai_system == 'gigachat' and len(ai_prompt) > 1:
            cls.send_action(user_id)
            GigaChat.add_message(user_id, "user", message, ai_prompt, cls.get_response)

        if ai_system == 'chatgpt':
            cls.send_action(user_id)
            ChatGpt.add_message(user_id, message, cls.get_response)

    @classmethod
    def get_response(cls, act_type=None, user_id=None, message=None):
        if act_type == "message":
            try:
                message = telegram_format(message)
                keyb = get_under_menu_buttons()
                cls._bot.send_message(user_id, message, reply_markup=keyb)
                cls.dialogues_new_message(F"ID: {user_id}\nBR: {message}")
            except Exception as e:
                lprint.p("Error on send message to user (bot_talks 59)", e)
        elif act_type == "action":
            cls.send_action(user_id)

    @classmethod
    def send_order(cls, message):
        spp = DatabaseCache.get_special_project_parameters(jinja=True)
        orders_chat_id = spp.get('ORDERS_CHATID_value')
        try:
            cls._bot.send_message(orders_chat_id, message)
        except Exception as e:
            lprint.p("Error on send message to ORDERS chat", e)

    @classmethod
    def send_order_confirmation(cls, message):
        try:
            spp = DatabaseCache.get_special_project_parameters(jinja=True)
            orders_chat_id = spp.get('ORDERS_CHATID_value')
            cls._bot.send_message(orders_chat_id, message)
        except Exception as e:
            lprint.p("Error on send message to ORDERS chat", e)

    @classmethod
    def voice_to_text(cls, user_id, voice):
        try:
            cls.send_action(user_id)
            spp = DatabaseCache.get_special_project_parameters(jinja=True)
            ai_system = spp.get('ai_system_value')
            # ai_prompt = spp.get('ai_system_extra_field_1') # Почему закомментировали?  Убрать или пояснить.
            # if ai_system == 'gigachat' and len(ai_prompt) > 1:
            #     return None
            if ai_system == 'chatgpt':
                return ChatGpt.voice_to_text(voice)
        except Exception as e:
            lprint.p("Error on voice to text", e)
        return None

    @classmethod
    def dialogues_new_message(cls, message):
        try:
            spp = DatabaseCache.get_special_project_parameters(jinja=True)
            dialogues_chat_id = spp.get('DIALOGUES_CHATID_value')
            if dialogues_chat_id:
                cls._bot.send_message(dialogues_chat_id, message)
        except Exception as e:
            lprint.p("Error on send message to DIALOGUES chat", e)

    @classmethod
    def get_tg_user_info(cls, user_id):
        try:
            return cls._bot.get_chat(user_id)
        except Exception as e:
            lprint.p("Error on get tg user info", e)
        return None

    @classmethod
    def send_message(cls, chat_id, message=None, image=None, video=None, reply_markup=None):
        try:
            if video or image:
                if image:
                    cls._bot.send_photo(chat_id, image, caption=message)
                if video:
                    if image:
                        cls._bot.send_video(chat_id, video)
                    else:
                        cls._bot.send_video(chat_id, video, caption=message)
            else:
                cls._bot.send_message(chat_id, message, reply_markup=reply_markup)
        except Exception as e:
            lprint.p("Error on send message to user (bot_talks 72)", e) # Что значит 72?
