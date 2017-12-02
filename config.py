import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "key"
    SECURITY_PASSWORD_SALT = "salty salt"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True

config = {
    "development": DevelopmentConfig,
    "production": Config
}