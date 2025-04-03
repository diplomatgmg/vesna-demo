import logging
import datetime
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO) # А если я debug хочу?


class lprint:

    logger = logging.getLogger("APP Logger")
    handler = TimedRotatingFileHandler("logs/app.log", when="midnight", interval=1, backupCount=7, encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    @classmethod
    def init(cls):
        cls.logger.setLevel(logging.INFO)
        cls.handler.setFormatter(cls.formatter)
        cls.logger.addHandler(cls.handler)
        cls.logger.info("Script started %s", datetime.datetime.now())

    @classmethod
    def p(cls, text, *args):
        cls.logger.info("%s %s", text, " ".join(map(str, args)))

    # почему debug, warning, error не используем?
