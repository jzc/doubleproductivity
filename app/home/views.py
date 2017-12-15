import os

from flask import render_template, send_from_directory, current_app

from . import home
from ..models import User, Post, Course
from flask_login import current_user, login_required

@home.route("/")
def show_home():
    courses = Course.query.all()
    return render_template("index.html", courses=courses)

@home.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(current_app.instance_path, "uploads"),
                            filename)
