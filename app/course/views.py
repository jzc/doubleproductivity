import re
import uuid
import os

from flask import abort, render_template, url_for, current_app, flash, redirect

from . import course
from .forms import ResourceUploadForm 
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

@course.route("/<course>/post/<id>")
def show_post(course, id):
    course = get_course(course)
    post = Post.query.get(id)
    return render_template("post.html",post=post)