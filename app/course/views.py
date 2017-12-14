import re
import os

from flask import abort, render_template, url_for, current_app, flash, redirect

from . import course
from .forms import ResourceUploadForm 
from .. import db, flash_errors
from ..models import Course, Resource

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
    return render_template("resources.html", resources=course.resources)
#     return """
# <object data="{0}" type="application/pdf" width="100%" height="100%">
#    <p><b>Example fallback content</b>: This browser does not support PDFs. Please download the PDF to view it: <a href="{0}">Download PDF</a>.</p>
# </object>
# """.format(url_for("home.download_file", filename=Resource.query.first().get_file_path()))


@course.route("/<course>/resources/upload", methods=["GET", "POST"])
def upload_resource(course):
    course = get_course(course)
    form = ResourceUploadForm()
    if form.validate_on_submit():
        file = form.resource.data
        resource = Resource(
            course=course,
            filename=file.filename,
            title=form.title.data,
            description=form.description.data
        )
        file.save(os.path.join(current_app.instance_path, "uploads", resource.upload_path))
        db.session.add(resource)
        db.session.commit()
        flash("Uploaded", "success")
        return redirect(url_for("course.show_resources", course="atoc1050"))
    flash_errors(form)
    return render_template("upload_resource.html", form=form)