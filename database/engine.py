import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

load_dotenv()

DB_NAME = str(os.getenv("db_name"))
DB_USER_NAME = str(os.getenv("db_user_name"))
DB_PASSWORD = str(os.getenv("db_password"))
DB_HOST = str(os.getenv("db_host"))
DB_PORT = str(os.getenv("db_port"))


class Engine:
    SQLALCHEMY_DATABASE_URL = F"postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" # можно использовать sqlalchemy.URL
    

    BASE = declarative_base()
    engine = create_engine(SQLALCHEMY_DATABASE_URL,
                           client_encoding='utf8',
                           pool_size=10,
                           max_overflow=100,
                           pool_recycle=60,
                           pool_pre_ping=True,
                           pool_timeout=15)
    fla_engine = create_engine(SQLALCHEMY_DATABASE_URL,
                               client_encoding='utf8',
                               pool_size=1,
                               max_overflow=100,
                               pool_recycle=60,
                               pool_pre_ping=True,
                               pool_timeout=15)

    @classmethod
    def get_engine(cls):
        return cls.engine

    @classmethod
    def get_db_session(cls):
        return scoped_session(sessionmaker(bind=cls.engine, expire_on_commit=False,
                                           autoflush=False))

    @classmethod
    def get_fla_session(cls):
        cls.fla_engine.dispose()
        return scoped_session(
            sessionmaker(bind=cls.fla_engine, expire_on_commit=True, autoflush=True))

    @classmethod
    def init_db(cls):
        cls.BASE.metadata.create_all(cls.get_engine())
