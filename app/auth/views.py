from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required

from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User, confirm_token
from .. import db

@auth.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = (User.query.filter(User.username.ilike(form.login.data)).first() or 
                User.query.filter(User.email.ilike(form.login.data)).first())
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Succsefully logged in.", "success")
            return redirect(request.args.get("next") or url_for("home.home"))
        flash("Invalid username or password", "error")
    return render_template("login.html", form=form)

@auth.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter(User.username.ilike(form.username.data)).first() is not None:
            flash("Username is already in use.", "error")
        elif User.query.filter(User.email.ilike(form.email.data)).first() is not None:
            flash("Email is already in use.", "error")
        else:
            new_user = User(email=form.email.data,
                            first=form.first.data,
                            last=form.last.data,
                            username=form.username.data,
                            password=form.password.data)

            db.session.add(new_user)
            db.session.commit()

            token = new_user.generate_confirmation_token()
            print(url_for("auth.confirm", token=token))
            return redirect(request.args.get("next") or url_for("home.home"))
    return render_template("register.html", form=form)

@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    error = False
    try:
        email = confirm_token(token)
        if email is None:
            error = True
    except:
        error = True
    if error:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for("home.home"))
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed. Please login.", "success")
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    return redirect(url_for("home.home"))

