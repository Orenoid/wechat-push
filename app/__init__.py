import logging

from flask import Flask
from flask.logging import default_handler

from app.blueprint import register_blueprint
from app.exception import BusinessLogicException, handle_business_exception, handle_base_exception
# from app.models import db
from config import config_map

from .utils import multilog


def create_app(config_name: str):

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # 写入日志文件
    app.logger.removeHandler(default_handler)
    handler = multilog.MyLoggerHandler('flask', encoding='UTF-8', when='H')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'
    )
    handler.setFormatter(logging_format)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    # 写入控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    app.logger.addHandler(ch)
    app.logger.setLevel(logging.INFO)

    @app.route('/', endpoint='ping_pong')
    def ping_pong():
        return "I'm still alive."

    # db.init_app(app)
    register_blueprint(app)
    app.register_error_handler(BusinessLogicException, handle_business_exception)
    app.register_error_handler(Exception, handle_base_exception)

    return app
