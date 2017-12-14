from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, TextAreaField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileRequired

class ResourceUploadForm(FlaskForm):
    title = TextField("Title", validators=[Required()])
    description = TextAreaField("Description", validators=[Required()])
    resource = FileField(validators=[FileRequired()])
    submit = SubmitField("Upload")