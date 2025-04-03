from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from database.engine import Engine


class ProductOrders(Engine.BASE):
    __tablename__ = "product_orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idempotence_key = Column(String(128), nullable=False, unique=True)
    payment_id = Column(String(128), nullable=False, unique=True)
    t_user_id = Column(BigInteger, nullable=False, unique=False)
    amount = Column(Integer, nullable=False)
    info_string = Column(String(4046), nullable=True)
    Created_At = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
