import re
import os

from flask import abort, render_template, url_for, current_app, flash, redirect, request
from flask_login import current_user, login_required

from . import course

from .forms import ResourceUploadForm, PostForm, CommentForm
from .. import db, flash_errors
from ..models import Course, Resource, Post, Comment

course_regex = re.compile("([A-Za-z]{4})([0-9]{4})")

def get_course(url):
    m = course_regex.match(url)
    q = Course.query.filter(Course.department.ilike(m.group(1)))
    if not q.first():
        abort(404)
    return q.filter_by(course_number=m.group(2)).first_or_404()

@course.errorhandler(401)
def unauth(e):
    flash("Must be logged in.", "error")
    return redirect(request.args.get("next") or url_for("home.show_home"))

@course.route("/<course>")
def show_course(course):
    course = get_course(course)
    return render_template("course_home.html", course=course)

@course.route("/<course>/resources")
def show_resources(course):
    course = get_course(course)
    return render_template("resources.html", resources=course.resources, course=course)

@course.route("/<course>/resources/upload", methods=["GET", "POST"])
@login_required
def upload_resource(course):
    course_url = course
    course = get_course(course)
    form = ResourceUploadForm()
    if form.validate_on_submit():
        file = form.resource.data
        resource = Resource(
            user=current_user,
            course=course,
            filename=file.filename,
            title=form.title.data,
            description=form.description.data
        )
        file.save(os.path.join(current_app.instance_path, "uploads", resource.uuid_filename))
        resource.make_thumb()
        db.session.add(resource)
        db.session.commit()
        flash("Uploaded", "success")
        return redirect(url_for("course.show_resources", course=course_url))
    flash_errors(form)
    return render_template("upload_resource.html", form=form)


@course.route("/<course>/post/<id>", methods=["POST","GET"])
def show_post(course, id):
    course_url = course
    course = get_course(course)
    post = Post.query.get(id)
    form = CommentForm()
    if not current_user.is_authenticated and request.method == "POST":
        flash("Must be logged in.", "error")
        return redirect(url_for("course.show_post", course=course_url, id=id))
    if form.validate_on_submit() and current_user.is_authenticated:
        c=Comment(post=post,user=current_user,content=form.content.data)
        db.session.add(c)
        db.session.commit()
        flash("Comment posted!", "success")
        return redirect(url_for("course.show_post", course=course_url, id=id))
    return render_template("post.html", post=post, form=form, course=course)

@course.route("/<course>/create_post", methods=["POST","GET"])
@login_required
def createPost(course):
    course_url = course
    course = get_course(course)
    print("hello")
    form = PostForm()
    if form.validate_on_submit():
        # logic for putting post in database
        # if (form.is_link):
        #     pass
            # check if content is a url
            
        new_post = Post(#is_link=form.is_link.data, 
                                title=form.title.data,
                                content=form.content.data, 
                                user=current_user,
                                #needs course info
                                course=course,
                                upvotes=0,
                                downvotes=0)
        db.session.add(new_post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for("course.show_post", course=course_url, id=new_post.id))
    return render_template("create_post.html", form=form, course=course)

@course.route("/<course>/members")
def showmembers(course):
    course=get_course(course)
    return render_template("members.html", course=course)