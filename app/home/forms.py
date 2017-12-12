from flask_wtf import FlaskForm
from wtforms.validators import Required
from wtforms import StringField, TextAreaField, RadioField, SelectField, SubmitField

class PostForm(FlaskForm):
	title = StringField("Title", validators=[Required()])
	content = TextAreaField("Content", validators=[Required()])
	is_link = RadioField("Post Type", choices=[(1, "Link Post"),(0, "Self Post")], validators=[Required()], coerce=int)
	course = SelectField("Class", choices=[(1, "1300"),(2,"3104"),(3,"2824")], validators=[Required()], coerce=int)
	category = SelectField("Category", choices=[(1,"Tutoring"),(2,"Question"),(3,"Bug Help")], validators=[Required()], coerce=int)
	submit = SubmitField("Post")
	
