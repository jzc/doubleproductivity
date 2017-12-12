from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User, confirm_token
from .. import db, flash_errors

@auth.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = (User.query.filter(User.username.ilike(form.login.data)).first() or 
                User.query.filter(User.email.ilike(form.login.data)).first())
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Succsefully logged in.", "success")
            return redirect(request.args.get("next") or url_for("home.show_home"))
        flash("Invalid username/email or password", "error")
    flash_errors(form)
    return render_template("login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home.show_home"))

@auth.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter(User.username.ilike(form.username.data)).first() is not None:
            flash("Username is already in use.", "error")
        elif User.query.filter(User.email.ilike(form.email.data)).first() is not None:
            flash("Email is already in use.", "error")
        else:
            new_user = User(
                email=form.email.data,
                first=form.first.data,
                last=form.last.data,
                username=form.username.data,
                password=form.password.data
            )

            db.session.add(new_user)
            db.session.commit()

            token = new_user.generate_confirmation_token()
            if current_app.testing:
                return "\nConfirmation URL: /confirm/%s\n" % token
            else:
                print(url_for("auth.confirm", token=token))
                flash("A confirmation email has been sent to you by email.", "success")
                return redirect(url_for("auth.login"))

    flash_errors(form)
    return render_template("register.html", form=form)

@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("home.show_home"))
    if current_user.confirm(token):
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "success")
    return redirect(url_for("home.show_home"))