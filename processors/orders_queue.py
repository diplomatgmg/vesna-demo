import threading
import datetime
from yookassa import Payment, Configuration
from database.engine import Engine
from processors.bot_talks import BotTalks
from database.models.orders import ProductOrders
from comon_functions.lprint import lprint


class OrdersProcessor:

    @classmethod
    def process_engine(cls):
        session = None
        try:
            if Configuration.account_id and Configuration.secret_key:
                session = Engine.get_db_session()
                orders = session.query(ProductOrders)
                for order in orders:
                    time_diff = datetime.datetime.now(datetime.timezone.utc) - order.Created_At
                    if time_diff > datetime.timedelta(hours=1):
                        lprint.p(f"OrdersProcessor: Deleting order {order.idempotence_key} older than 1 hours.")
                        session.delete(order)
                        message = F"Заказ {order.info_string} {order.idempotence_key} <strong>УДАЛЕН</strong>"
                        BotTalks.send_order_confirmation(message)
                    else:
                        try:
                            payment = Payment.find_one(order.payment_id)
                            if payment.status == "succeeded":
                                message = F"Заказ {order.info_string} {order.idempotence_key} <strong>Оплачен</strong>"
                                BotTalks.send_order_confirmation(message)
                                BotTalks.send_message(order.t_user_id, F"Заказ {order.info_string} <strong>Оплачен</strong>.")
                                session.delete(order)
                        except Exception as e:
                            lprint.p("OrdersProcessor: error when get payment status.", e)
                session.commit()
                session.close()
            else:
                lprint.p("OrdersProcessor: Configuration not found")
        except Exception as e:
            lprint.p("Error in orders processor", e)
        finally:
            if session:
                session.close()
        threading.Timer(60, cls.process_engine, args=()).start()

    @classmethod
    def init(cls):
        threading.Timer(10, cls.process_engine, args=()).start()
