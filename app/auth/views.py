from flask import render_template, redirect, request, url_for
from flask_login import login_user

from . import auth
from .forms import LoginForm
from ..models import User

@auth.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("bla")
        user = User.query.filter(User.username.ilike(form.username.data)).first()
        print(user)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or url_for("home.home"))
        flash("Invalid username or password", "error")
    return render_template("login.html", form=form)

@auth.route("/register", methods=["POST", "GET"])
def register():
    pass