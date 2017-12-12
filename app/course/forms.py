from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired

class ResourceUploadForm(FlaskForm):
    resource = FileField(validators=[FileRequired()])
    submit = SubmitField("Upload")

