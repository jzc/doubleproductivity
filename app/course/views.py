import re
import uuid
import os

from flask import abort, render_template, url_for, current_app, flash, redirect
from flask_login import current_user, login_required

from . import course
from .forms import ResourceUploadForm, PostForm 
from .. import db
from ..models import Course, Resource, Post

course_regex = re.compile("([A-Za-z]{4})([0-9]{4})")

def get_course(url):
    m = course_regex.match(url)
    q = Course.query.filter(Course.department.ilike(m.group(1)))
    if not q.first():
        abort(404)
    return q.filter_by(course_number=m.group(2)).first_or_404()

@course.route("/<course>")
def show_course(course):
    course = get_course(course)
    return render_template("course_home.html", course=course)

@course.route("/<course>/resources")
def show_resources(course):
    course = get_course(course)
    return """
<object data="{0}" type="application/pdf" width="100%" height="100%">
   <p><b>Example fallback content</b>: This browser does not support PDFs. Please download the PDF to view it: <a href="{0}">Download PDF</a>.</p>
</object>
""".format(url_for("home.download_file", filename=Resource.query.first().get_file_path()))


@course.route("/<course>/resources/upload", methods=["GET", "POST"])
def upload_resource(course):
    course = get_course(course)
    form = ResourceUploadForm()
    if form.validate_on_submit():
        file = form.resource.data
        fuuid = str(uuid.uuid4())
        filename, ext = os.path.splitext(file.filename)
        resource = Resource(
            course=course,
            filename=filename+ext, 
            uuid=fuuid
        )
        file.save(os.path.join(current_app.instance_path, "uploads", fuuid+ext))
        db.session.add(resource)
        db.session.commit()
        flash("Uploaded", "success")
        return redirect(url_for("course.show_resources", course="atoc1050"))

    return render_template("upload_resource.html", form=form)

@course.route("/<course>/create_post", methods=["POST","GET"])
@login_required
def createPost(course):
    course = get_course(course)
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
                                course=course,
                                upvotes=0,
                                downvotes=0)
        db.session.add(new_post)
        db.session.commit()

        raise Exception
    return render_template("create_post.html", form=form)