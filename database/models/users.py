from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from database.engine import Engine


class Users(Engine.BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    t_user_id = Column(BigInteger, unique=True, index=True, nullable=False)
    t_username = Column(String(256))
    t_first_name = Column(String(256))
    t_last_name = Column(String(256))
    t_is_premium = Column(Boolean, default=False)
    password = Column(String(256), nullable=True)
    email = Column(String(256), unique=True, nullable=True)
    phone = Column(String(16), unique=True, nullable=True)
    Created_At = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    Updated_At = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
