from . import db

# Model - User
# id
# email
# first 
# last
# screen name - unique
# password (stored in hash)
# score/rep
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    first = db.Column(db.String(32))
    last = db.Column(db.String(32))
    screen_name = db.Column(db.String(20))

# Model - UserCourse
# id
# UserId
# ClassId

# Model - Course
# id
# department
# course number
# course name

# Model - Post
# id
# isLink
# content
# CourseID 
# VotableID

# Model - Comment
# id
# VotableID

# Model - Votable
# id
# upvotes 
# downvotes