from flask import render_template
from .forms import PostForm
from . import home
from ..models import User, Post
from flask_login import current_user, login_required

@home.route("/")
def homeIndex():
    return render_template("index.html", posts=Post.query.all()[:10])
    
@home.route("/create_post", methods=["POST","GET"])
@login_required
def createPost():
    print("hello")
    form = PostForm()
    if form.validate_on_submit():
        # logic for putting post in database
        if (form.is_link):
            pass
            # check if content is a url
            
        new_post = Post(is_link=form.is_link.data, 
                                title=form.title.data,
                                content=form.content.data, 
                                user=current_user,
                                #needs course info
                                upvotes=0,
                                downvotes=0)
        db.session.add(new_post)
        db.session.commit()

        raise Exception
        pass
    return render_template("create_post.html", form=form)

# @home.route("/thing/<screen_name>")
# def user(screen_name):
#     if screen_name in [user.screen_name for user in User.query.all()]:
#         return "Hello, %s" % screen_name
#     else: 
#         return "User not found"

