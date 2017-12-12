import unittest
import re

from app.models import User
from app import create_app, db

class AuthViewTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data)

    def test_login_logout(self):
        u = User(username="user", email="user@colorado.edu", password="password")
        db.session.add(u)
        db.session.commit()

        #test logout with login
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 401)

        #test invalid login
        response = self.client.post("/login", data={
            "login": "notuser",
            "password": "password"
        })
        self.assertIn(b"Invalid username/email or password", response.data)

        response = self.client.post("/login", data={
            "login": "notuser@colorado.edu",
            "password": "password"
        })
        self.assertIn(b"Invalid username/email or password", response.data)

        response = self.client.post("/login", data={
            "login": "user",
            "password": "notpassword"
        })
        self.assertIn(b"Invalid username/email or password", response.data)  

        response = self.client.post("/login", data={
            "login": "user@colorado.edu",
            "password": "notpassword"
        })
        self.assertIn(b"Invalid username/email or password", response.data) 

        #test incomplete form
        s1 = b"Email or username - This field is required."
        s2 = b"Password - This field is required."
        response = self.client.post("/login", data={})
        self.assertIn(s1, response.data) 
        self.assertIn(s2, response.data)

        response = self.client.post("/login", data={
            "login": "user"
        })
        self.assertIn(s2, response.data)
        
        response = self.client.post("/login", data={
            "password": "password"
        })
        self.assertIn(s1, response.data)

        #test login and logout w/ username
        response = self.client.post("/login", data={
            "login": "user",
            "password": "password"
        }, follow_redirects=True)
        self.assertIn(b"Succsefully logged in.", response.data)

        response = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"You have been logged out.", response.data)
        self.assertIn(b"login", response.data)

        #test login and logout w/ email
        response = self.client.post("/login", data={
            "login": "user@colorado.edu",
            "password": "password"
        }, follow_redirects=True)
        self.assertIn(b"Succsefully logged in.", response.data)

        response = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"You have been logged out.", response.data)
        self.assertIn(b"login", response.data)

        db.session.delete(u)
        db.session.commit()

    def test_register_confirm(self):
        u = User(
            first="John",
            last="Doe",
            email="john.doe@colorado.edu",
            username="john.doe",
            password="password"
        )
        db.session.add(u)
        db.session.commit()

        #test incomplete form
        response = self.client.post("/register")
        required = [
            b"First name - This field is required.",
            b"Last name - This field is required.",
            b"Username - This field is required.",
            b"Email - This field is required.",
            b"Password - This field is required.",
            b"Confirm password - This field is required."
        ]
        for s in required:
            self.assertIn(s, response.data)
        
        #test username in use
        response = self.client.post("/register", data={
            "first": "John",
            "last": "Doe",
            "username": "john.doe",
            "email": "john.doe1@colorado.edu",
            "password": "password",
            "confirm_password": "password"
        })
        self.assertIn(b"Username is already in use.", response.data)

        #test email in use
        response = self.client.post("/register", data={
            "first": "John",
            "last": "Doe",
            "username": "john.doe1",
            "email": "john.doe@colorado.edu",
            "password": "password",
            "confirm_password": "password"
        })
        self.assertIn(b"Email is already in use.", response.data)

        #test email regex
        response = self.client.post("/register", data={
            "first": "John",
            "last": "Doe",
            "username": "john.doe1",
            "email": "john.doe1@notcolorado.edu",
            "password": "password",
            "confirm_password": "password"
        })
        self.assertIn(b"Must be a colorado.edu email.", response.data)
        
        #test confirm password
        response = self.client.post("/register", data={
            "first": "John",
            "last": "Doe",
            "username": "john.doe1",
            "email": "john.doe1@colorado.edu",
            "password": "password",
            "confirm_password": "notpassword"
        })
        self.assertIn(b"Confirm password - Field must be equal to password.", response.data)

        #test successful register
        response = self.client.post("/register", data={
            "first": "John",
            "last": "Doe",
            "username": "john.doe1",
            "email": "john.doe1@colorado.edu",
            "password": "password",
            "confirm_password": "password"
        }, follow_redirects=True)
        m = re.search("Confirmation URL: (/confirm/.+)", response.data.decode("utf8"))
        self.assertIsNotNone(m)
        new_user = User.query.filter_by(username="john.doe1").first()
        self.assertIsNotNone(new_user)
        self.assertFalse(new_user.confirmed)
    
        self.client.post("/login", data={
            "login": "john.doe1",
            "password": "password"
        })
        #test confirm
        response = self.client.get("confirm/abc", follow_redirects=True)
        self.assertIn(b"The confirmation link is invalid or has expired.", response.data)

        response = self.client.get(m.group(1), follow_redirects=True)
        self.assertIn(b"You have confirmed your account. Thanks!", response.data)
        self.assertTrue(new_user.confirmed)

