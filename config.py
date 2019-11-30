import os
from app.utils.encoder import CustomEncoder

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    RESTFUL_JSON = {'cls': CustomEncoder}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WECHAT_TOKEN = os.environ.get('WECHAT_TOKEN')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "PRO_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "dev-data.sqlite")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


config_map = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
