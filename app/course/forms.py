from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, TextField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileRequired

class ResourceUploadForm(FlaskForm):
    title = TextField("Title", validators=[Required()])
    description = TextAreaField("Description", validators=[Required()])
    resource = FileField(validators=[FileRequired()])
    submit = SubmitField("Upload")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[Required()])
    content = TextAreaField("Content", validators=[Required()])
    is_link = BooleanField("Link Post")
    course = SelectField("Class", choices=[(1, "1300"),(2,"3104"),(3,"2824")], validators=[Required()], coerce=int)
    category = SelectField("Category", choices=[(1,"Tutoring"),(2,"Question"),(3,"Bug Help")], validators=[Required()], coerce=int)
    submit = SubmitField("Post")
class CommentForm(FlaskForm):
    content=TextAreaField("Content", validators=[Required()])
    submit = SubmitField("Submit")
