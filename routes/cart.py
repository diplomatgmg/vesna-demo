import json
import uuid
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Blueprint, render_template, redirect, request
import yookassa
from yookassa import Payment, Configuration
from database.engine import Engine
from database.cache import DatabaseCache
from database.models.orders import ProductOrders
from pydantic_store.schemas import CartFormItems, CartFromProductData
from comon_functions.lprint import lprint
from processors.bot_talks import BotTalks
from config.config import PROJECT_RANDOM_ID

cart_router = Blueprint("cart_router", __name__)


@cart_router.route("/cart", methods=["GET"])
def cart_page():
    try:
        products = DatabaseCache.get_products_on_main()
        actions = DatabaseCache.get_special_project_parameters_actions()
        context = {
            "title": "Корзина",
            "meta_description": "Корзина",
            "meta_keywords": "cart, page",
            "project_random_id": PROJECT_RANDOM_ID,
            "page": "cart",
            "products": products[:2],
            "actions": actions,
        }
        context.update(DatabaseCache.get_special_project_parameters(jinja=True))

    except Exception as e:
        lprint.p("Error on product page", e)
        return render_template("error.html")

    return render_template("cart.html", **context)


@cart_router.route("/cart", methods=["POST"])
def cart_send():

    try:
        form_data = request.form.copy()
        products_data = json.loads(form_data.get('products')[:1024])
        products_data = [CartFromProductData(**product) for product in products_data]
        del form_data['products']
        cart_data = form_data
        cart_data = CartFormItems(**cart_data)

        spp = DatabaseCache.get_special_project_parameters(jinja=True)
        actions = DatabaseCache.get_special_project_parameters_actions()

        if cart_data.payment_type == "delivery" and spp.get(
                "cart_allow_post_payment_value") == "yes":
            delivery_price = int(spp.get("cart_delivery_price_offline_value") or 999)
        elif cart_data.payment_type == "online":
            delivery_price = int(spp.get("cart_delivery_price_value") or 999)
        else:
            delivery_price = 9999

        calculated_discount = 0
        calculated_total = 0
        items_total = 0

        selected_products = []
        for product in products_data:
            p = DatabaseCache.get_product_by_id(product.product_id)
            selected_products.append({
                "product":
                p,
                "parameter": [
                    parameter for parameter in p.parameters
                    if parameter.Parameter_ID == product.parameter_id
                ][0],
                "quantity":
                product.quantity
            })

        the_messahe = "Новый заказ\n"
        the_info_string = ""
        for product in selected_products:
            items_total += product['quantity']
            calculated_total += product['parameter'].price * product['quantity']
            the_messahe += F"{product['product'].Product_Name}, {product['parameter'].name} {product['parameter'].parameter_string} - {product['quantity']}шт\n"
            the_info_string += F"{product['product'].Product_Name}\n"
        the_messahe += "\nДанные клиета\n"
        for v1, v2 in cart_data:
            the_messahe += F"{v1}: {v2}\n"

        for action in actions:
            if action.action_type == "p23":
                v1 = int(action.extra_field_1 or 0)
                v2 = int(action.extra_field_2 or 0)
                if items_total == 2 and v1 != 0:
                    calculated_discount += round(calculated_total / 100 * v1)
                elif items_total >= 3 and v2 != 0:
                    calculated_discount += round(calculated_total / 100 * v2)
        calculated_total -= calculated_discount
        calculated_total += delivery_price
        order_total = calculated_total
        if cart_data.payment_type == "delivery" and spp.get(
                "cart_allow_post_payment_value") == "yes":
            calculated_total = delivery_price

        the_messahe += "\nИтог\n"
        if delivery_price != 0:
            the_messahe += F"Стоимость доставки: {delivery_price} руб.\n"
        if calculated_discount != 0:
            the_messahe += F"Сумма скидки: {calculated_discount} руб.\n"
        the_messahe += F"К оплате: {calculated_total} руб.\n"
        the_messahe += F"Общая сумма заказа: {order_total} руб.\n"
        the_info_string += F"Оплата: {calculated_total}р. Сумма:{order_total}р. Скидка: {calculated_discount}р.\n"

        the_messahe += "\nТех. Инфо\n"
        idempotence_key = str(uuid.uuid4())
        if not Configuration.account_id or not Configuration.secret_key:
            the_messahe += "WARNING: <strong>Заказ не отправлен на оплату в связи с тем, что ненайдены данные магазина!</strong>" # Не очень грамотно поставлена речь. "не найдены"
            BotTalks.send_order(the_messahe)
            return redirect("/")

        payment = Payment.create(
            {
                "amount": {
                    "value": calculated_total,
                    "currency": "RUB"
                },
                # "payment_method_data": {
                #     "type": "sbp"
                # },
                "confirmation": {
                    "type": "redirect",
                    "return_url": spp.get('yokassa_return_url_value', "/")
                },
                "capture": True,
                "description": F"Заказ {idempotence_key}"
            },
            idempotence_key)
        payment_link = payment.confirmation.confirmation_url

        try:
            tg_user = BotTalks.get_tg_user_info(cart_data.tg_user_id)
            if tg_user:
                the_messahe += F"TGU: @{tg_user.username}\n"
                the_messahe += F"TGU: {tg_user.first_name} {tg_user.last_name}\n"
                markup = InlineKeyboardMarkup(row_width=1)
                markup.add(InlineKeyboardButton(text="ОПЛАТИТЬ", url=payment_link))
                BotTalks.send_message(tg_user.id,
                                      "Спасибо за заказ, оставляю ссылку на оплату.",
                                      reply_markup=markup)
                session = Engine.get_db_session()
                new_order = ProductOrders(idempotence_key=idempotence_key,
                                          payment_id=payment.id,
                                          t_user_id=tg_user.id,
                                          amount=calculated_total,
                                          info_string=the_info_string)
                session.add(new_order)
                session.commit()
                session.close()
        except Exception as e:
            lprint.p("Error receiving tg user info", e)

        the_messahe += F"IDKEY: {idempotence_key}\n"
        the_messahe += F"PID: {payment.id}\n"
        the_messahe += F"URL: {payment_link}\n"
        BotTalks.send_order(the_messahe)

        context = {
            "title": "ССылка на оплату", # почему две заглавных буквы
            "meta_description": "ССылка на оплату", # аналогично
            "meta_keywords": "payment, page",
            "project_random_id": PROJECT_RANDOM_ID,
            "page": "payment_link",
            "payment_link": payment_link,
        }
        context.update(DatabaseCache.get_special_project_parameters(jinja=True))
        return render_template("cart_link_page.html", **context)

    except Exception as e:
        lprint.p("Error on form data", e)
        redirect("/cart")

    return redirect("/")
