import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Regexp, EqualTo

email_regex = re.compile("^[a-zA-Z0-9_.+-]+@colorado.edu$", flags=re.I)

class LoginForm(FlaskForm):
    login = StringField("Email or username", validators=[Required()])
    password = PasswordField("Password", validators=[Required()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    first = StringField("First name", validators=[Required()])
    last = StringField("Last name", validators=[Required()])
    username = StringField("Username", validators=[Required()])
    email = StringField("Email", validators=[Required(), Regexp(email_regex, message="Must be a colorado.edu email.")])
    password = PasswordField("Password", validators=[Required()])
    confirm_password = PasswordField("Confirm password", validators=[Required(), EqualTo("password")])
    submit = SubmitField("Register")