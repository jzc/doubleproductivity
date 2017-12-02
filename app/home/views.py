from flask import render_template

from . import home
from ..models import User, Post

@home.route("/")
def home():
    return render_template("index.html", posts=Post.query.all()[:10])

# @home.route("/thing/<screen_name>")
# def user(screen_name):
#     if screen_name in [user.screen_name for user in User.query.all()]:
#         return "Hello, %s" % screen_name
#     else: 
#         return "User not found"