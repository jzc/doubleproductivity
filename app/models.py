from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

from . import db, login_manager



user_course = db.Table("user_course",
                       db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
                       db.Column("course_id", db.Integer, db.ForeignKey("courses.id"), primary_key=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return None
    return email

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean)
    email = db.Column(db.String, unique=True)
    first = db.Column(db.String)
    last = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    courses = db.relationship("Course", secondary=user_course)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        return URLSafeTimedSerializer(current_app.config['SECRET_KEY']).dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    def confirm(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        if email != self.email:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String)
    course_number = db.Column(db.Integer)
    course_name = db.Column(db.String)
    users = db.relationship("User", secondary=user_course)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    is_link = db.Column(db.Boolean)
    title = db.Column(db.String)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="posts")
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    course = db.relationship("Course", backref="posts")
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    post = db.relationship("Post", backref="comments")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="comments")
    content = db.Column(db.String)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
