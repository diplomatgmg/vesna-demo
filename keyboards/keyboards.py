from telebot.types import InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from database.cache import DatabaseCache
from comon_functions.lprint import lprint


def get_start_menu_buttons():
    return [
        # InlineKeyboardButton(text="Узнать больше", callback_data="about_extra"), # Почему закомментировали? Уберите или добавьте пояснение
        InlineKeyboardButton(text="Открыть приложение 🏪",
                             web_app=WebAppInfo(url=DatabaseCache.get_special_project_parameters(
                                 jinja=True).get('webapp_link_value'))),
    ]


def get_under_menu_buttons_text() -> list:
    filtered_buttons = []
    try:
        spp = DatabaseCache.get_special_project_parameters(jinja=True)
        btns = spp.get('under_menu_buttons_description').split('\n')
        for button in btns:
            cleaned_button = button.replace("\r", "").strip()
            if len(cleaned_button) > 0:
                filtered_buttons.append(cleaned_button)
    except Exception as e:
        lprint.p("Error on get_under_menu_buttons_text", e)
    return filtered_buttons


def get_under_menu_buttons() -> ReplyKeyboardMarkup:
    new_buttons = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    for button in get_under_menu_buttons_text():
        btn_cmd, btn_text = button.split("#") if len(button.split("#")) == 2 else [None, None]
        if btn_text:
            if btn_cmd == "app":
                try:
                    new_buttons.append(
                        KeyboardButton(
                            text=btn_text, # Ошибка типа
                            web_app=WebAppInfo(url=DatabaseCache.get_special_project_parameters(
                                jinja=True).get('webapp_link_value'))))
                except Exception as e:
                    lprint.p("Error on get_under_menu_buttons", e)
            if btn_cmd == "sup":
                new_buttons.append(KeyboardButton(text=btn_text)) # ошибка типа
    markup.add(*new_buttons)
    return markup
