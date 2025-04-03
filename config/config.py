import os
from dotenv import load_dotenv
from yookassa import Configuration
from database.cache import DatabaseCache


load_dotenv() # В точке входа - app.py мы уже подгружаем env, зачем еще раз?

GIGACHAT_AUTH_DATA: str = str(os.getenv("gigachat_auth_data"))


def init_conf():
    spp = DatabaseCache.get_special_project_parameters(jinja=True)
    Configuration.account_id = spp.get("SHOP_YOKASSA_value")
    Configuration.secret_key = spp.get("SHOP_YOKASSA_extra_field_1")


try:
    with open(".build", "r", encoding="utf-8") as f:
        PROJECT_RANDOM_ID = int(f.readline())
        PROJECT_RANDOM_ID += 1
except Exception: # Почему любые ошибки перехватываются, с чем это связано?? Оставили бы тогда просто except, зачем Exeption добавлять?
    PROJECT_RANDOM_ID = 0


with open(".build", "w", encoding="utf-8") as f:
    f.write(str(PROJECT_RANDOM_ID))
