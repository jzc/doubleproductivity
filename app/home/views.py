from flask import render_template

from . import home
from ..models import User, Post

@home.route("/")
def home():
    posts = Post.query.all()
    posts = [p for p in posts if len(p.title.split()) < 15]
    return render_template("index.html", posts=posts)