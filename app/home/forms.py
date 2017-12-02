from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SelectField
class PostForm(FlaskForm):
	title = StringField("Title")
	content = TextAreaField("Content")
	is_link = RadioField("Post Type", choices=[(True, "Link Post"),(False, "Self Post")])
	course = SelectField("Class", choices=[("", "1300"),("","3104"),("","2824")])
	category = SelectField("Category", choices=[("","Tutoring"),("","Question"),("","Bug Help")])
	
