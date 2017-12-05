import re

from flask import abort, render_template

from . import course
from .. import db
from ..models import Course

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