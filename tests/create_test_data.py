import os
import random
import csv
import shutil

def create_test_data(db, models):
    db.drop_all()
    db.create_all()

    # create some courses
    courses = []
    with open("%s/courses.csv" % os.path.dirname(__file__)) as f:
        next(f)
        for line in f:
            tokens = line.strip().split(",")
            data = {
                "department": tokens[0],
                "course_number": tokens[1],
                "course_name": tokens[2],
            }
            c = models["Course"](**data)
            courses.append(c)
            db.session.add(c)

    # create some users
    users = []
    words = [line.strip() for line in open("%s/words.txt" % os.path.dirname(__file__), "r")]
    n_users = 1000
    for i in range(n_users):
        first = random.choice(words)
        last = random.choice(words)
        username = "%s.%s" % (first, last)
        data = {
            "first": first,
            "last": last,
            "username": username,
            "email": "%s@%s.com" % (username, random.choice(words)),
            "courses": random.sample(courses, random.randint(1, 5)),
        }
        u = models["User"](**data)
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
        p = models["Post"](**data)
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
        c = models["Comment"](**data)
        db.session.add(c)


    admin = models["User"](
        first="Admin",
        last="Nimda",
        email="admin@admin.com", 
        confirmed=True,
        username="admin",
        password="password"
    )

    db.session.add(admin)

    shutil.rmtree("instance/uploads")
    os.mkdir("instance/uploads")
    algo = models["Course"].query.filter_by(course_name="Algorithms").first()
    with open("%s/resources.csv" % os.path.dirname(__file__)) as f:
        r = csv.reader(f)
        for title, description, filename in r:
            r = models["Resource"](
                course=algo,
                user=admin,
                filename=filename,
                title=title,
                description=description
            )
            shutil.copyfile("tests/resources/"+filename, "instance/uploads/"+r.uuid_filename)
            r.make_thumb()

    db.session.commit()