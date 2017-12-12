import os

from flask import Flask, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .course import course as course_blueprint
    app.register_blueprint(course_blueprint, url_prefix="/course")

    return app

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s - %s" % (getattr(form, field).label.text, error), "error")