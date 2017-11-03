import sys
sys.path.append('..')

import random

from app import create_app

with create_app("development").app_context():
    from app import db
    from app.models import *
    db.drop_all()
    db.create_all()
    # create some courses
    courses = []

    with open("course.csv") as f:
        next(f)
        for line in f:
            tokens = line.strip().split(",")
            data = {
                "department": tokens[0],
                "course_number": tokens[1],
                "course_name": tokens[2],
            }
            c = Course(**data)
            courses.append(c)
            db.session.add(c)

    # create some users
    users = []
    words = [line.strip() for line in open("words.txt", "r")]
    n_users = 1000
    for i in range(n_users):
        first = random.choice(words)
        last = random.choice(words)
        screen_name = "%s.%s" % (first, last)
        data = {
            "first": first,
            "last": last,
            "screen_name": screen_name,
            "email": "%s@%s.com" % (screen_name, random.choice(words)),
            "courses": random.sample(courses, random.randint(1, 5)),
        }
        u = User(**data)
        users.append(u)
        db.session.add(u)

    # create some posts
    posts = []
    n_posts = 1000
    for i in range(n_posts):
        data = {
            "is_link": False,
            "title": ' '.join(random.sample(words, random.randint(1, 50))),
            "content": ' '.join(random.sample(words, random.randint(10,100))),
            "upvotes": random.randint(10,100),
            "downvotes": random.randint(0,20),
            "user": random.choice(users),
            "course": random.choice(courses),
        }
        p = Post(**data)
        posts.append(p)
        db.session.add(p)

    # create some comments
    n_comments = 1000
    for i in range(n_comments):
        data = {
            "content": ' '.join(random.sample(words, random.randint(1,50))),
            "upvotes": random.randint(10,100),
            "downvotes": random.randint(0,20),
            "post": random.choice(posts),
            "user": random.choice(users),
        }
        c = Comment(**data)
        db.session.add(c)

    db.session.commit()