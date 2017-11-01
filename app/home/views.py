from flask import render_template

from . import home
from ..models import User

@home.route("/")
def home():
    return render_template("index.html", users=User.query.all())