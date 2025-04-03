import time
import threading
import os

from flask import Flask
import telebot
from waitress import serve
from dotenv import load_dotenv

from database.engine import Engine
from database.models.special_project_parameters import SpecialProjectParameters
from database.models.special_project_parameters_badges import SpecialProjectParametersBadges
from database.models.special_project_parameters_actions import SpecialProjectParametersActions
from database.models.products import Products
from database.models.product_images import ProductImages
from database.models.product_colors import ProductColors
from database.models.product_marks import ProductMarks
from database.models.product_mark_assignments import ProductMarkAssignments
from database.models.product_importance import ProductImportance
from database.models.categories import Categories
from database.models.product_categories import ProductCategories
from database.models.product_extra import ProductExtra
from database.models.orders import ProductOrders
from database.models.product_reviews import ProductReviews
from database.models.product_reviews_video import ProductReviewsVideo
from database.models.product_parameters import ProductParameters
from database.models.product_parameters_assignments import ProductParameterAssignments
from database.models.users import Users

from database.cache import DatabaseCache
from config import config

from comon_functions.lprint import lprint
from comon_functions.jinja_filters import nl2br

from processors.orders_queue import OrdersProcessor

from processors.bot_talks import BotTalks
from scenario.begin import send_welcome
from scenario.other_messages_handler import handle_other_text, moderator_join_chat_hadler, moderator_exit_handler

from routes.index import index_router
from routes.product import product_router
from routes.products import products_router
from routes.stock import stock_router
from routes.cart import cart_router

load_dotenv()

fl_app = Flask(__name__)
bot = telebot.TeleBot(str(os.getenv("TOKEN")), parse_mode="HTML", num_threads=4)


def run_flask():
    from admin_ext.main import FlaskAdmin
    lprint.p("Flask server start")
    fl_app.config['SECRET_KEY'] = 'A23049564219WOFH21355'
    fl_app.config['BASIC_AUTH_USERNAME'] = 'admin'
    fl_app.config['BASIC_AUTH_PASSWORD'] = str(os.getenv("ADMIN_PASS"))
    fl_app.config['BASIC_AUTH_REALM'] = 'Authentication Required'
    FlaskAdmin.init()
    FlaskAdmin.fl_admin.init_app(fl_app)
    fl_app.register_blueprint(index_router)
    fl_app.register_blueprint(product_router)
    fl_app.register_blueprint(products_router)
    fl_app.register_blueprint(stock_router)
    fl_app.register_blueprint(cart_router)
    fl_app.jinja_env.filters['nl2br'] = nl2br
    # fl_app.run(host='127.0.0.1', port=5777, debug=False, threaded=False)
    serve(fl_app, host='0.0.0.0', port=5777, threads=8)


def run_telebot():
    bot.register_message_handler(send_welcome, commands=['start'], pass_bot=True)
    bot.register_message_handler(moderator_exit_handler, commands=['moderator_exit'], pass_bot=True)
    bot.register_callback_query_handler(moderator_join_chat_hadler,
                                        func=lambda call: call.data.startswith("support_message_"),
                                        pass_bot=True)
    bot.register_message_handler(handle_other_text, content_types=['text', 'voice', 'photo'], pass_bot=True)
    lprint.p("Telebot server start")
    bot.infinity_polling()


if __name__ == "__main__":
    Engine.init_db()
    config.init_conf()
    lprint.init()
    BotTalks.init(bot)
    OrdersProcessor.init()
    if str(os.getenv("bot_disable")) != "1":
        telebot_thread = threading.Thread(target=run_telebot, daemon=True)
        telebot_thread.start()
    time.sleep(0.5)
    if str(os.getenv("flask_disable")) != "1":
        run_flask()
    if str(os.getenv("bot_disable")) != "1":
        bot.stop_polling()
        telebot_thread.join()
