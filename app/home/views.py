from flask import render_template

from . import home
from ..models import User, Post

@home.route("/")
def home():
    posts = Post.query.all()
    posts = [p for p in posts if len(p.title.split()) < 15]
    return render_template("index.html", posts=posts)

# @home.route("/thing/<screen_name>")
# def user(screen_name):
#     if screen_name in [user.screen_name for user in User.query.all()]:
#         return "Hello, %s" % screen_name
#     else: 
#         return "User not found"