import os

from flask import render_template, send_from_directory, current_app

from . import home
from ..models import User, Post

@home.route("/")
def show_home():
    posts = Post.query.all()
    posts = [p for p in posts if len(p.title.split()) < 15]
    return render_template("index.html", posts=posts)

@home.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(current_app.instance_path, "uploads"),
                            filename)